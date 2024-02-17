# Why Kafka is Fast
## Sequential I/O

Kafka relies heavily on the filesystem for storing and caching messages. 

There is a general perception that “disks are slow”, which means high seek time. Imagine if we can avoid seek time, we can achieve low latency as low as RAM here. 

Kafka does this through Sequential I/O.

Fundamental to Kafka is the concept of the log: an append-only, totally ordered data structure, similar to the [Write-Ahead Log](https://github.com/xinrong-databricks/knowledge-sharing/blob/master/System/18.%20PostgreSQL%20Study.md#write-ahead-log) discussed before.

Producer append at the end of the log stream in immutable and monotonic fashion and consumers can maintain their own pointers to indicate current message processing.

Every time producer publish a message it gets acknowledgement containing record’s offset. First record published to partition gets offset as 0, second as 1 and so on in an ever-increasing sequence. 

Consumers consume data from a position specified by an offset and then save their position in a log by committing periodically. Purpose of saving offset is to let another consumer resume from its position in case consumer instance crashes.

## Zero Copy

What happens when we fetch data from memory/disk and send it over the network.

- To fetch data, it copies data from the Kernel Context into the Application Context.
- To send those data to the Internet, it copies data from the Application Context into the Kernel Context.

Each time data traverses the user-kernel boundary, copying the data consumes CPU cycles and memory bandwidth. 

![image](https://user-images.githubusercontent.com/47337188/178143837-219fc44a-67cd-4caa-b705-11d6bda41e5b.png)

Here zero copy comes into stage.

Applications that use zero copy request that the kernel copy the data directly from the disk file/memory to the socket, without going through the application.

![image](https://user-images.githubusercontent.com/47337188/178143853-2b2af431-0b06-4c2c-9724-566769cce026.png)


## Batch Data and Compression
Efficient compression requires compressing multiple messages together rather than compressing each message individually.

Kafka supports this by allowing recursive message sets*. A batch of messages can be clumped together compressed and sent to the server in this form. This batch of messages will be written in compressed form and will remain compressed in the log and will only be decompressed by the consumer.

Assuming the bandwidth is 10MB/s, sending 10MB data in one go is much faster than sending 10000 messages one by one(assuming each message takes 100 bytes).

Compression will improve the consumer throughput for some decompression cost.

**Message sets**

One structure common to both the produce and fetch requests is the message set format. 

A message in kafka is a key-value pair with a small amount of associated metadata. A message set is just a sequence of messages with offset and size information. This format happens to be used both for the on-disk storage on the broker and the on-the-wire format.

A message set is also the unit of compression in Kafka, and we allow messages to recursively contain compressed message sets to allow batch compression.


## Horizontally Scaling
**Partition**

Note that having broken a topic up into partitions, we need a way of deciding which messages to write to which partitions. 

Typically, if a message has no key, subsequent messages will be distributed round-robin among all the topic’s partitions. 
In this case, all partitions get an even share of the data, but we don’t preserve any kind of ordering of the input messages. 

If the message does have a key, then the destination partition will be computed from a hash of the key. 
This allows Kafka to guarantee that messages having the same key always land in the same partition, and therefore are always in order.

**Consumer Group**

The main way we scale data consumption from a Kafka topic is by adding more consumers to the consumer group.

![image](https://user-images.githubusercontent.com/47337188/178144586-83ab18a5-f9bc-4ffc-88c3-a4afe43bed90.png)

**Replication**

In Kafka, replication happens at the partition granularity.

For every partition, there is a replica that is designated as the leader. The Leader is responsible for sending as well as receiving data for that partition. All the other replicas are called the in-sync replicas (or followers) of the partition.

![image](https://user-images.githubusercontent.com/47337188/178144884-7e0e29d9-e525-4853-b99b-5af3c5703bb3.png)

Now let’s see what happens when a broker goes down. If for some reason lets say Broker 2 goes down. The access to partition 1 is now lost since broker 2 was the leader for partition 1.

What happens now is Kafka automatically selects one of the in-sync replicas (in our case there is only 1 replica) and makes them the leader.

Producers can choose to receive acknowledgements for the data writes to the partition using the “acks” setting.


## *References
https://medium.com/@sunny_81705/what-makes-apache-kafka-so-fast-71b477dcbf0#:~:text=Sequential%20I%2FO%3A,this%20through%20Sequential%20I%2FO.

https://developer.ibm.com/articles/j-zerocopy/

https://catherine-shen.medium.com/scale-kafka-consumers-481be563bf3c

https://developer.confluent.io/learn-kafka/apache-kafka/partitions/#kafka-partitioning

https://medium.com/@_amanarora/replication-in-kafka-58b39e91b64e
