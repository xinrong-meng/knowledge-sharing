# Event Streaming Platform

Today, data is in motion, and engineering teams need to model applications to process business requirements as streams of events, not as data at rest, sitting idly in a traditional data store.

## Apache Kafka

Apache Kafka is an open-source distributed event streaming platform.

![IMG_9151](https://user-images.githubusercontent.com/47337188/178081742-ae481549-6c63-4357-935f-9f1340244f61.jpg)

We can regard Producer and Consumer as clients, Brokers as servers.

A Kafka cluster consists of multiple Brokers. 

Topic is partitioned; Broker hosts partitions.

<img width="539" alt="image" src="https://user-images.githubusercontent.com/47337188/178082095-be145207-3408-4574-8a1c-ce650fff9535.png">

Partition is replicated; One replica is leader.

<img width="539" alt="image" src="https://user-images.githubusercontent.com/47337188/178082694-76adad28-c529-49c3-8a37-e603a8ad379d.png">

There is an offset associated with each message.

<img width="541" alt="image" src="https://user-images.githubusercontent.com/47337188/178082742-01751511-6e5d-456d-8cd6-b8395ba68de9.png">

A request from Producer looks like "Write data to topic A partition 2".

<img width="540" alt="image" src="https://user-images.githubusercontent.com/47337188/178082869-56f738fe-6105-4cdb-a27a-76971b179667.png">

Kafka consumers are typically part of a consumer group . When multiple consumers are subscribed to a topic and belong to the same consumer group, each consumer in the group will receive messages from a different subset of the partitions in the topic.

There is a consumer coordinator to manage the assignment

## Common Architecture

An example model looks as below

![image](https://user-images.githubusercontent.com/47337188/177908147-08e60b67-b681-41f7-8a90-9eabad2a5b74.png)

We can design business processes and applications around Event Streams. Everything, from sales, orders, trades, and customer experiences to sensor readings and database updates, is modeled as an Event. Events are written to the Event Streaming Platform once, allowing distributed functions within the business to react in real time. Systems external to the Event Streaming Platform are integrated using Event Sources and Event Sinks. Business logic is built within Event Processing Applications, which are composed of Event Processors that read events from and write events to Event Streams.

### Table

#### Projection Table

How can a stream of change events be efficiently summarized to give the current state of the world?

![image](https://user-images.githubusercontent.com/47337188/178018024-2567badb-9df6-4a8e-8214-db5646ad7a2b.png)

We can maintain a projection table that behaves just like a materialized view in a traditional database. 

As new events come in, the table is automatically updated, constantly giving us a live picture of the system. 

Events with the same key are considered related; newer events are interpreted, depending on their contents, as updates to or deletions of older events.

As with a materialized view, projection tables are read-only. To change a projection table, we change the underlying data by recording new events to the table's underlying stream.

ksqlDB supports easy creation of summary tables and materialized views. We declare them once, and the server will maintain their data as new events stream in.

#### State Table

How can an Event Processor manage mutable state, similar to how a table does in a relational database?

![image](https://user-images.githubusercontent.com/47337188/178017305-b9e743b1-f0a0-4fe8-8b10-f185d7c44b55.png)

Event Processors often need to perform stateful operations, such as an aggregation (for example, counting the number of events). The state is similar to a table in a relational database, and is mutable: it allows for read and write operations. 

It is essential that the event processor has an efficient and fault-tolerant mechanism for state management--for recording and updating the state while processing input events--to ensure correctness of the computations and to prevent data loss and data duplication.

We need to implement a mutable state table that allows the Event Processor to record and update state. For example, to count the number of payments per customer, a state table provides a mapping between the customer (for example, a customer ID) and the current count of payments.

The state's storage backend can vary by implementation: options include local state stores (such as RocksDB), remote state stores (such as Amazon DynamoDB or a NoSQL database), and in-memory caches. Local state stores are usually recommended, as they do not incur additional latency for network round trips, and this improves the end-to-end performance of the Event Processor.

The streaming database ksqlDB provides state tables out of the box with its TABLE data collection. The implementation uses local, fault-tolerant state stores that are continuously backed up into ksqlDB's distributed storage layer -- Kafka -- so that the data is durable.


## *References
https://developer.confluent.io/patterns/event-stream/event-streaming-platform/

https://www.instaclustr.com/blog/apache-kafka-architecture/

https://ksqldb.io/

https://kafka.apache.org/intro


