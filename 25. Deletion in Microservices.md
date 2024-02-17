# Deleting data in Microservices Architecture

## Introduction
Microservices architectures tend to distribute responsibility for data throughout an organization. This poses challenges to ensuring that data is deleted.

Even though each microservice is intended to be de-coupled and autonomous, it doesn't mean that it's completely independent from a data perspective. 

Coordination and communication is necessary if we want to preserve some level of referential integrity. Referential integrity is the logical dependency of a foreign key on a primary key.

**Solution 1: Just Delete It**

![image](https://user-images.githubusercontent.com/47337188/173153921-c0e3d7ff-9f2d-4280-bf5c-1bfc4b299eb8.png)
Cons: no referential integrity

**Solution 2: Synchronous Coordination**

![image](https://user-images.githubusercontent.com/47337188/173155457-0debc66a-cd5f-4892-a8c4-432a9caf90c4.png)
Cons: an increase in complexity, additional latency per request, compromised availability

**Solution 3: Just Don't Delete**

Instead of supporting a true "delete", the Product service would just expose a "decommission" endpoint for a product, but preserve the data in its database. 

In this way, the Catalog and Order Services would no longer have orphaned data

Cons: same as above (since it introduces a synchronous dependence from the Catalog Service to the Product Service).

**Solution 4: Asynchronous Update**

To support the Catalog Service's autonomy, instead of relying on the Product Service it could maintain its own local cache of product data, keeping it sync with changes from the Product Service. 

When a product is decommissioned, the Product Service could emit a ProductDecommissioned event which the Catalog Service would listen for, and then it could update its own local product store.

But what exactly is this local cache of product data?

- if in-memory

cons: small data only; no referential integrity

- if database

cons: complexity, synchronization (multiple instances of a given microservice share one database instance)

- if Event Log

[TBD] Event-Driven Microservices

## Learning from Twitter's erasure pipeline

An erasure pipeline includes data discovery, access, and processing

- Discovery

First, you’ll need to find the data that needs to be deleted. Data about a given event, user, or record could be in online or offline datasets, and may be owned by disparate parts of your organization.

So your first job will be to use your knowledge of your organization, the expertise of your peers, and organization-wide communication channels to compile a list of all relevant data.

- Access and processing

The data you find will usually be accessible to you in one of three ways. 

Online data will be mutable via (1) a real-time API or (2) an asynchronous mutator. 

Offline warehoused data will be mutable via (3) a parallel-distributed processing framework like MapReduce.

For (2): Your erasure pipeline can publish erasure events to a distributed queue, like Kafka, which partner teams subscribe to in order to initiate data deletion. They process the erasure event and call back to your team to confirm that the data was deleted.

For (3): You can provide an offline dataset which partner teams use to remove erasable data from their datasets. This offline dataset can be as simple as persisted logs from your erasure event publisher.

**An Erasure Pipeline**

The erasure pipeline we’ve described thus far has a few key requirements. It must:

- Accept incoming erasure requests
- Track and persist which pieces of data have been deleted
- Call synchronous APIs to delete data
- Publish erasure events for asynchronous erasure
- Generate an offline dataset of erasure events

An example erasure pipeline looks like
![image](https://user-images.githubusercontent.com/47337188/173157874-36621edd-9329-4aae-905d-67a83f491ef3.png)



## References
https://blog.twitter.com/engineering/en_us/topics/infrastructure/2020/deleting-data-distributed-throughout-your-microservices-architecture

https://www.bennorthrop.com/Essays/2021/microservices-architecture-and-deleting-data.php

https://www.ibm.com/docs/en/informix-servers/14.10?topic=integrity-referential
