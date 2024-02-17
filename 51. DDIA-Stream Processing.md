# Stream Processing

In general, a “stream” refers to data that is **incrementally made available over time**. The concept appears in many 
places: in the stdin and stdout of Unix, programming languages (lazy lists), filesystem APIs (such as Java’s 
FileInputStream), TCP connections, delivering audio and video over the internet, and so on.

In this chapter we will look at **event streams** as a **data management** mechanism.

## 1. Transmitting Event Streams

A common approach for notifying consumers about new events is to use a messaging system: a producer sends a message 
containing the event, which is then **pushed** to consumers.

Within this publish/subscribe model, different systems take a wide range of approaches. To differentiate the systems,
it is particularly helpful to ask the following two questions:
- What happens if the producers send messages faster than the consumers can process them?
  - drop messages
  - buffer messages in a queue
  - apply backpressure (also known as flow control; i.e., blocking the producer from sending more messages)
- What happens if nodes crash or temporarily go offline—are any messages lost?
  - writing to disk
  - replication
  - afford to sometimes lose messages
  
### Message brokers
A widely used alternative is to send messages via a message broker (also known as a message queue), which is 
essentially a kind of database that is optimized for handling message streams. It runs as a server, with producers 
and consumers connecting to it as clients.

By centralizing the data in the broker, these systems can more easily tolerate clients that come and go (connect, 
disconnect, and crash), and the question of **durability** is moved to the broker instead.

A consequence of queueing is also that consumers are generally **asynchronous**: when a producer sends a message, it 
normally only waits for the broker to confirm that it has buffered the message and does not wait for the message to 
be processed by consumers.

#### AMQP/JMS-style message broker

The broker assigns individual messages to consumers, and consumers acknowledge individual messages when they have 
been successfully processed. Messages are deleted from the broker once they have been acknowledged.

RabbitMQ and Azure Service Bus are AMQP/JMS-style message brokers.

#### Log-based message broker

The broker assigns all messages in a partition to the same consumer node, and always delivers messages in the same 
order.

Parallelism is achieved through partitioning. Within each partition, the broker assigns a monotonically increasing sequence number, or **offset**, to every
**message**. There is **no ordering guarantee across different partitions**. Consumers track their progress by 
checkpointing the **offset** of the last message they have processed.

The broker retains messages on disk, so it is possible to jump back and reread old messages if necessary.

A **topic** can then be defined as **a group of partitions** that all carry messages of the same type, as shown below.

![image](https://user-images.githubusercontent.com/47337188/227669705-09cccfd4-05c8-4c88-860e-c04e4ddba8cd.png)

Apache Kafka and Amazon Kinesis Streams are log-based message brokers.

## 2. Databases and Streams

we saw that log-based message brokers have been successful in taking ideas from databases and applying them to 
messaging. We can also go in reverse: take **ideas from messaging and streams**, and apply them **to databases**.

We said previously that an **event** is a record of something that happened at some point in time. The thing that 
happened may be a user action (e.g., typing a search query), or a sensor reading, but it may also be **a write to a** 
**database**.

Representing databases as streams opens up powerful opportunities for **integrating systems**. You can keep derived 
data systems such as search indexes, caches, and analytics systems continually up to date by consuming the log of 
changes and applying them to the derived systems.

## 3. Processing Streams

There are 3 options to process streams:

- You can take the data in the events and **write** it to a database, cache, search index, or similar storage system, 
  from where it can then be **queried** by other clients.
- You can **push** the events **to users** in some way, for example by sending email alerts or push notifications, or by 
  streaming the events to a real-time dashboard where they are visualized. In this case, a human is the ultimate 
  consumer of the stream.
- You can process one or more input streams to **produce** one or more output **streams**. Streams may go through a pipeline 
  consisting of several such processing stages before they **eventually end up at an output** (option 1 or 2). A 
  piece of code that processes streams like this is known as an **operator** or a **job**.

### Reasoning About Time

Stream processors often need to deal with **time**. 

Many stream processing frameworks use the **local system clock** on the processing machine (**the processing time**) to 
determine windowing.

A tricky problem when defining windows in terms of **event time** is that you can never be sure when you have received 
all of the events for a particular window, or whether there are some events still to come.

Assigning timestamps to events is even more difficult when events can be buffered at several points in the system.

To adjust for incorrect device clocks, one approach is to log 3 timestamps:

1. The time at which the event **occurred**, according to the device clock
2. The time at which the event was **sent** to the server, according to the device clock
3. The time at which the event was **received** by the server, according to the server clock

By subtracting the second timestamp from the third, you can estimate the offset between the **device clock** and the 
**server clock** (assuming the network delay is negligible compared to the required timestamp accuracy). You can then 
apply that offset to the event timestamp, and thus estimate the **true time at which the event actually occurred**.

#### Types of windows

Once you know how the **timestamp** of an event should be determined, the next step is to decide how windows over **time** 
**periods** should be defined. The window can then be used for **aggregations**, for example to count events, or to 
calculate the average of values within the window.

- Tumbling window

A tumbling window has a **fixed length**, and every event belongs to **exactly one** window.
For example, if you have a 1-minute tumbling window, all the events with timestamps between 10:03:00 and 10:03:59 
are grouped into one window, events between 10:04:00 and 10:04:59 into the next window, and so on.

- Hopping window

A hopping window also has a **fixed length**, but allows windows to **overlap**.
For example, a 5-minute window with a hop size of 1 minute would contain the events between 10:03:00 and 10:07:59, 
then the next window would cover events between 10:04:00 and 10:08:59, and so on.

- Sliding window

A sliding window is bound by time, but its endpoints are determined by user activity. So you create your stream and 
set a maximum time difference between two records that will allow them to be included in the first window.

- Session window

Unlike the other window types, a session window has **no fixed duration**. Instead, it is defined by grouping 
together all events for the **same user** that occur closely together in time, and the window ends when the user has 
been inactive for some time (for example, if there have been no events for 30 minutes). Sessionization is a common 
requirement for website analytics.

**Hopping windows vs. Sliding windows**

For hopping windows, the window is **re-evaluated** on fixed time intervals, independent of the actual content of the 
data stream. You could use a hopping window if you need to get **periodic** results. 
For example:a daily business report over the last seven days; or an hourly update over the last 24h. Even if no new 
record are processed, you want to get a result in fixed time intervals sent downstream.

On the other hand, a sliding window is **re-evaluated** only if the content of the window changes, ie, each time a new 
record enters or leaves the window. This type of window is good for a “**moving average**” computation as an example.

See more https://developer.confluent.io/learn-kafka/kafka-streams/windowing/ for Kafka windowing.

### Stream Joins

The fact that new events can appear anytime on a stream makes joins on streams more challenging than in batch jobs.

We distinguish three types of joins that may appear in stream processes:

- Stream-stream joins

**Both** input streams consist of **activity events**, and the join operator searches for **related events** that occur 
within some window of time. For example, it may match two actions taken by the same user within 30 minutes of each 
other.

- Stream-table joins

**One** input stream consists of **activity events**, while the other is a **database changelog**. The changelog 
keeps a local copy of the database up to date. For each activity event, the join operator queries the database and 
outputs an **enriched** activity event.

For example, two datasets: a set of user activity events and a database of user profiles. It is natural to think of 
the user activity events as a stream, and to perform the **join** on a **continuous** basis in a stream 
processor:the input is a stream of activity events containing a user ID, and the output is a stream of activity 
events in which the user ID has been **augmented** with profile information about the user.

- Table-table joins (materialized view maintenance)

**Both** input streams are **database changelogs**. In this case, every **change** on one side is joined with the 
latest state of the other side. The result is a stream of **changes** to the materialized view of the join between the 
two tables.

Consider the Twitter timeline example. When a user wants to view their home timeline, it is too expensive to iterate 
over all the people the user is following, find their recent tweets, and merge them.
Instead, we want a **timeline cache**: a kind of **per-user** “inbox” to which tweets are written as they are sent, so that 
reading the timeline is a single lookup.
To implement this cache maintenance in a stream processor, you need streams of **events** for tweets (sending and 
deleting) and for follow relationships (following and unfollowing).
The stream process needs to maintain a database containing the set of followers for each user so that it knows which 
timelines need to be updated when a new tweet arrives.

Another way of looking at this stream process is that it maintains a materialized view for a query that joins two 
tables (tweets and follows), something like the following:

```sql
SELECT follows.follower_id AS timeline_id,
array_agg(tweets.* ORDER BY tweets.timestamp DESC)
FROM tweets
JOIN follows ON follows.followee_id = tweets.sender_id
GROUP BY follows.follower_id
```
The join of the streams corresponds directly to the join of the tables in that query. The timelines are effectively 
a cache of the result of this query, updated every time the underlying tables change.

#### Stream vs. Table (in Kafka)

**Streams** are unbounded series of events, while **tables** are the current state of a given key. Both streams and tables
are built from Apache Kafka topics; the difference is only the semantic interpretation of the data. Which you choose
is determined by how you want to use the data.

![image](https://user-images.githubusercontent.com/47337188/230692830-96ad8809-ae31-4f4c-9b73-5b4029e06d2c.png)

Taking the chess board example in the graphic above, a single Kafka topic would hold the history of all the moves.

- A ksqlDB stream on that topic would apply a schema to it, and from that you could replay some or all of the game, or 
identify any events involving a specific piece or square.
- A ksqlDB table on the same topic would apply a schema to it and tell you the current location of each piece. Each 
time a piece moves (and a new event is written to the Kafka topic), the table updates its state.

### Fault Tolerance

The same issue of fault tolerance arises in stream processing, but it is less straightforward to handle: waiting 
until a task is finished before making its output visible is not an option, because a stream is infinite and so you 
can never finish processing it.

#### Microbatching and checkpointing

One solution is to break the stream **into small blocks**, and treat each block like a miniature batch process. This 
approach is called microbatching, and it is used in Spark Streaming.

Microbatching also implicitly provides a **tumbling window** equal to the batch size (windowed by processing time, not 
event timestamps); any jobs that require larger windows need to explicitly carry over state from one microbatch to 
the next.

By maintaining a strong ordering on the processing of batches and storing the batch ID information with your state, 
you can know whether or not the batch has been processed before. This allows you to avoid ever applying updates 
multiple times, thereby achieving exactly-once semantics.

A variant approach, used in Apache Flink, is to periodically generate **rolling checkpoints** of state and write them to 
**durable** storage. If a stream operator crashes, it can **restart** from its most recent checkpoint and discard any 
output generated between the last checkpoint and the crash.

## References

Designing Data-Intensive Applications By Martin Kleppmann

https://forum.confluent.io/t/sliding-windows-vs-hopping-windows/882

https://developer.confluent.io/learn-kafka/kafka-streams/windowing/

https://developer.confluent.io/learn-kafka/ksqldb/streams-and-tables/
