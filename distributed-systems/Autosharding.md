# Autosharding

Autosharding primarily refers to the automatic partitioning of data across multiple servers or databases, as part of 
a strategy to improve scalability, performance, and availability in distributed systems. It's mostly discussed in 
the context of data management within databases or data storage systems.

However, the principles behind autosharding can also influence service sharding, albeit indirectly and under a 
broader category known as "automatic scaling" or "auto-scaling" in service architectures.

## Slicer: Auto-Sharding for Datacenter Applications

Slicer emerges as a highly sophisticated, **general-purpose** sharding service developed by Google. It's designed to 
**dynamically** partition workloads across servers in datacenter applications to optimize performance, **scalability**, 
and **availability**.

### 1. Core Principles

- General Purpose Sharding Service: Slicer is not limited to specific types of applications or data. It can be applied 
universally, much like a filesystem or lock manager, providing a broad utility across Google's diverse ecosystem.

- Dynamic Work Distribution: It constantly monitors load and server health to adaptively distribute workloads. This 
dynamism ensures that Slicer can respond to changing conditions, such as load spikes or server failures, in real-time.

- High Availability and Load Balancing: One of Slicer's primary goals is to maintain high availability and evenly 
  distribute load across tasks, reducing resource wastage and improving system responsiveness.

### 2. How It Works

<img width="871" alt="image" src="https://gist.github.com/assets/47337188/42b2fae7-e098-447e-93fa-6732287fb6bc">

Slicer has the following components:

- Slicer Service: The central component that generates and manages shard assignments.
- Clerk: A client library that interacts with the Slicer Service to obtain shard-to-task mappings.
- Slicelet: A server library that informs server tasks about their shard assignments.

A **shard/slice** is a portion of a dataset or workload.

A **(server) task** is an instance of a service running on a server that is designated to perform a specific set of 
operations or tasks. Each server task is responsible for handling a specific shard or set of shards.

The Slicer Service generates an assignment mapping key ranges (“slices”) to tasks and distributes it to the Clerks
and Slicelets, together called the subscribers. The Clerk **directs** client requests for a key to the assigned task. The
Slicelet **enables a task to learn** when it is assigned or relieved of a slice. The Slicer Service **monitors** load and
task availability to generate new assignments to maintain availability of all keys.

Application code interacts only indirectly with the Slicer Service via the Clerk and Slicelet libraries.

#### 2.1 Why these 3 components

The division into these three components allows Slicer to separate concerns effectively.

- The Slicer Service acts as the central authority for shard assignment decisions. This centralized approach allows 
for a **global view** of the system's state, enabling intelligent decisions about workload distribution across server 
tasks.

- Clerks are necessary to **abstract the complexity** of shard management away from the client applications. By 
integrating with the client side, Clerks allow applications to interact with the sharded system without needing 
detailed knowledge of the underlying shard assignments.

- Slicelets are essential for managing the **dynamic** nature of shard assignments on the server side. Without them, 
server tasks would not be able to adapt to changes in shard assignments, leading to potential imbalances or 
inefficiencies.

#### 2.2 Slicer Service

#### Fault Tolerance

The **Assigner** is a core component of the Slicer Service, acting as the central authority responsible for generating 
shard assignments.

**Distributors** serve as the intermediary layer that conveys the shard assignments from the Assigner to the Clerks and 
Slicelets within the system.

| Strategy    | Details                                                                                                                                                   | Benefit                                                                                                         |
|-----------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------|
| Geographic Diversity        | Slicer runs Assigners and Distributors across multiple data centers globally.                                                                                             | Ensures operational continuity in the face of machine, data center, and network failures.                      |
| Backup Assignment Retrieval | Includes a Backup Distributor mechanism that serves assignments directly from persistent storage if the primary path fails.                                              | Provides a robust failover mechanism, ensuring availability even if the primary distribution network is down.  |
| Assignment Caching | Assignments are distributed to Clerks and Slicelets and are cached locally.                                    | Allows system to continue routing requests correctly based on the last known shard assignments during failures.|

#### Load Balancing

Minimize load imbalance across server tasks to optimize performance and resource utilization. Imbalance is measured 
as the ratio of the maximum task load to the mean task load across all tasks.

Slicer employs a sophisticated algorithm for load balancing that considers current load distributions and 
**dynamically** adjusts shard (slice) assignments to achieve optimal load distribution. This involves:

Slicer’s initial assignment divides the keyspace equally among available tasks, assuming that key load is uniform 
(key distribution is uniform due to hashing).

Slicer monitors key load – either request rate, which can be automatically tracked via the Slicelet integration with 
Stubby, or application reported custom metrics – to determine if load balancing changes are required

Slicer also limits key churn, the fraction of the key space affected by reassignment. Key churn itself creates load 
and increases overhead.

#### Strong Consistency

Slicer can be configured to ensure that at no point will there be ambiguity about which task a shard (slice) is 
assigned to. This means that every task knows precisely which shards it's responsible for, and there's a system-wide 
agreement on these assignments.

### 3. Uses in Production Systems

| Use Case Category       | Example Applications | Description                                                                                                                                                                                                 |
|-------------------------|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| In-memory Cache         | Flywheel             | Enhances website reachability detection by ensuring updates and requests converge on a single task.                                                                                                         |
|                         | Meeting Scheduler    | Manages meetings and provides faster responses through per-user caching.                                                                                                                                    |
|                         | Crawl Manager        | Manages crawl rate-limiting by retaining last crawl times per URL.                                                                                                                                           |
|                         | Fonts Service        | Caches font files for web and mobile applications.                                                                                                                                                           |
| In-memory Store         | Speech Recognition   | Assigns languages to tasks, dynamically adjusting resources based on language demand.                                                                                                                        |
|                         | Cloud DNS            | Dynamically assigns DNS records to tasks for quick, in-memory handling of DNS requests.                                                                                                                      |
| Aggregation Applications| Event Analysis       | Supports systems building models from event sources, enabling efficient write aggregation and model caching.                                                                                                 |
|                         | Client Push          | A pub/sub system for mobile devices, where Slicer enables efficient topic-based message distribution and subscription management.                                                                            |

### 4. Conclusions

Slicer is a highly available, low-latency, scalable and adaptive sharding service that remains decoupled from 
customer binaries and offers optional assignment consistency.

## References

ChatGPT 4

https://www.usenix.org/system/files/conference/osdi16/osdi16-adya.pdf


