# Design A Key-value Store

A key-value store is a non-relational database where unique keys are paired with values, accessed via the key. Keys 
can be plain text (e.g., “last_logged_in_at”) or hashed (e.g., “253DDEC4”). Values, which may be strings, lists, or 
objects, are treated as opaque data in systems like Amazon Dynamo, Memcached, and Redis.

We are designing a key-value store that supports two operations:
- put(key, value) - inserts a value associated with a key.
- get(key) - retrieves the value associated with a key.

## Understand the problem and establish design scope

- Small key-value pairs (less than 10 KB).
- Ability to store big data.
- High availability, ensuring fast responses even during failures.
- Highly scalable, able to grow with large data sets.
- Automatic server scaling based on traffic.
- Adjustable consistency levels.
- Low latency.

### Single server key-value store

Use a hash table to store key-value pairs in memory, as memory access is fast. However, due to memory limitations, 
it may be impossible to store all data. Two optimizations can help:

- Data compression
- Store only frequently used data in memory and the rest on disk

### Distributed key-value store

A distributed key-value store, also known as a distributed hash table, spreads key-value pairs across multiple servers. 

#### CAP theorem

The CAP theorem states that a distributed system can only provide two out of three properties at the same time:

- Consistency: consistency means all clients see the same data at the same time no matter which node they connect to.

- Availability: availability means any client which requests data gets a response even if some of the nodes are down.

- Partition Tolerance: a partition indicates a communication break between two nodes. Partition tolerance means the 
system continues to operate despite network partitions.

Key-value stores are classified based on the two CAP characteristics they support.

- CP (consistency and partition tolerance) systems: a CP key-value store supports consistency and partition tolerance 
while sacrificing availability.

- AP (availability and partition tolerance) systems: an AP key-value store supports availability and partition 
tolerance while sacrificing consistency.

- CA (consistency and availability) systems: a CA key-value store supports consistency and availability while 
sacrificing partition tolerance. Since network failure is unavoidable, a distributed system must tolerate network partition.
Thus, a CA system cannot exist in real-world applications.

Choosing the right CAP guarantees that fit your use case is an important step in building a distributed key-value store.

## System components

### Data partition

For large applications, storing all data on a single server isn’t feasible. A common solution is to split the data 
into smaller partitions and store them across multiple servers. However, two challenges arise:

- Even data distribution across servers.
- Minimizing data movement when servers are added or removed.

Consistent hashing is a technique that addresses these challenges.

### Data replication

To ensure high availability and reliability, data is replicated asynchronously across N servers, where N is a 
configurable parameter.

Replicas are placed in distinct data centers, and data centers are connected through high-speed networks.

### Consistency

To synchronize data across replicas in a distributed system, **quorum consensus** is used to ensure consistency for 
both read and write operations.

- N: The number of replicas.
- W: Write quorum size. A write is successful when acknowledged by at least W replicas.
- R: Read quorum size. A read is successful when responses from at least R replicas are received.

Trade-off between latency and consistency:
- W = 1 or R = 1: Faster operation because the system only waits for one replica to respond.
- W > 1 or R > 1: Better consistency but slower due to waiting for more replicas to respond.

If W + R > N, strong consistency is guaranteed because at least one replica will have the most recent data. 
Otherwise, consistency might not be guaranteed.

How to configure N, W, and R to fit our use cases? Here are some of the possible setups:

- If R = 1 and W = N, the system is optimized for a fast read.
- If W = 1 and R = N, the system is optimized for fast write.
- If W + R > N, strong consistency is guaranteed (Usually N = 3, W = R = 2).
- If W + R <= N, strong consistency is not guaranteed.

#### Consistency models

A consistency model defines the degree of data consistency:

- Strong consistency: any read operation returns a value corresponding to the result of the most updated write data 
item. A client never sees out-of-date data.

- Weak consistency: subsequent read operations may not see the most updated value.

- Eventual consistency: this is a specific form of weak consistency. Given enough time, all updates are propagated, 
and all replicas are consistent.


### Inconsistency resolution

Replication gives high availability but causes inconsistencies among replicas. Versioning and vector locks are used 
to solve inconsistency problems. Versioning means treating each data modification as a new immutable version of data.

A vector clock is a [server, version] pair associated with a data item. It can be used to check if one version 
precedes, succeeds, or in conflict with others.

Each node maintains its own local vector clock for each data item, reflecting its view of the update history. Vector 
clocks are distributed across nodes and are synchronized through communication, ensuring each node progressively 
builds a consistent view of data history across replicas.

### Handling failures

#### Failure detection

In distributed systems, marking a server as down requires multiple independent confirmations, as relying on a single 
server’s report can be unreliable. All-to-all multicasting can help but is inefficient in large systems. A more 
effective approach is the gossip protocol.

In a gossip protocol, each node typically maintains a membership list that includes all nodes in the system, along 
with basic information such as node IDs and heartbeat counters. This list allows each node to know about the 
existence and status of every other node, helping detect which nodes are active or potentially offline.

#### Handling temporary failures

Sloppy Quorum improves availability by relaxing strict quorum rules:

- Temporary Substitution: Instead of enforcing quorum, the system selects the first W healthy servers for writes and 
R healthy servers for reads, ignoring down servers.
- Hinted Handoff: If a primary server is down, a healthy server temporarily processes requests. Once the down server 
  is back, the data is handed off to restore consistency.

#### Handling permanent failures

We implement an anti-entropy protocol to keep replicas in sync. Anti-entropy involves comparing each piece of data 
on replicas and updating each replica to the newest version. A Merkle tree (or hash tree)  is used for inconsistency detection and 
minimizing the amount of data transferred.

- Each leaf node in a Merkle tree contains the hash of a data block (e.g., a data bucket).
- Each non-leaf node holds the hash of its child nodes, combining and summarizing the hashes of data blocks below it.

Merkle trees allow data synchronization to be proportional to the differences between replicas, not the total data volume.

#### Handling data center outage

Replicate data across multiple data centers.

## System architecture diagram

Since the chapter is premium content, to respect copyright, please refer to 
https://bytebytego.com/courses/system-design-interview/design-a-key-value-store.

## References

https://bytebytego.com/courses/system-design-interview/design-a-key-value-store

ChatGPT 4o