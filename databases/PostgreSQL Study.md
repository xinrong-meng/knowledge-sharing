# PostgreSQL Study

## Recap: Relational Model

This model organizes data into one or more **tables** of columns and rows, with a **unique key** identifying each row.

Here, Table == Relation, Row == Record == Tuple, Column == Attribute.

Each **table** represents one "entity **type**".

The **rows** represent **instances** of that type of entity and the columns represent values attributed to that instance.

## PostgreSQL

It is an object-relational database management system (ORDBMS).

In addition to storing data in rows and tables in a database, PostgreSQL is capable of storing data as **objects** in a database.

Objects are models that contain data (**attributes**), and code (**methods**). They allow for **complex** models to be developed in software.

PostgreSQL offers built-in data types that are more complex than a relational database, such as xml and json. It also allows you to create custom data types. These custom types inherit all of the properties of the **object** that they are **based** off of.

Now let’s have an overview of PostgreSQL’s architecture. There are 3 main components: Memory, Processes and Physical Files.



![alt_text](https://user-images.githubusercontent.com/47337188/162540882-10068098-d5fd-42c7-9451-749b33fc70e8.png "PostgreSQL architecture")


Here we focus on Memory and Processes.

### Memory

Memory in PostgreSQL can be classified into two categories: Local Memory and Shared Memory.


![alt_text](https://user-images.githubusercontent.com/47337188/162540955-6e0eb550-ec77-40b6-896b-a19e1e259334.png "Processes, Memory and Data")



#### Local Memory

Local memory is allocated by **each** backend **process** for its own use. Below are parameters for local memory management.



* **Work_mem** is for sort (e.g. ORDER BY, DISTINCT) and hash (e.g. hash joins) operations.
* **Maintenance_work_mem** is for maintenance operations such as VACUUM.
* **Temp_buffers** sets the maximum number of temporary buffers used by each database session. The session local buffers are used only for access to temporary tables.


#### Shared Memory

Shared memory is used by **all processes** of a PostgreSQL server.



* **Shared Buffers** are for quick access to data.

  The data that is written or modified in this location is called "**dirty data**".

  Subsequently, the dirty data is written to disk containing physical files to record the data.

  These files are called Data Files.

* **Write Ahead Log (WAL) Buffers** are for backup and recovery.

  This WAL data is the metadata about changes to the actual data.


* **Commit Log Buffers** differ from the WAL, they have the commit status of all transactions.

  Commit logs are designed for PostgresSQL internals, so users cannot read them. PostgreSQL server access this folder to take the decision like which transaction completed or which did not.


### Processes

There are mainly 4 different types of Processes:



* **Postmaster Process**

  It is the **first** process started when you start PostgreSQL.

  It performs recovery, **initializes** **shared memory** and runs **background processes**.
 
  It also creates a **backend** **process** when there is a connection request from the **client process**.

* **Background Process**
* **Backend Process**

  The backend process performs the **query** request of the client process and then transmits the result.

* **Client Process**


## Write-Ahead Log

WAL persists every **state chang**e to the **append-only** **log**.



![alt_text](https://user-images.githubusercontent.com/47337188/162541029-8b192264-ece8-452c-9bbd-7d42b37799ca.png "WAL")


The log file can be read on every **restart** and the state can be **recovered** by replaying all the log entries.

Using WAL results in a significantly reduced number of disk writes, because only the log file needs to be flushed to disk to guarantee that a transaction is committed, rather than every data file changed by the transaction.


### Flushing

It's important to make sure that entries written to the log file are persisted on the physical media.

Flushing **every** log **write** to the disk gives a strong **durability** guarantee, but this **limits performance** and can quickly become a bottleneck. If flushing is **delayed** or done **asynchronously**, it improves performance but there is a risk of losing entries from the log if the server crashes before entries are flushed.

Most implementations use techniques like **Batching**, to limit the impact of the flush operation.


### Segmented Log

A single log file can grow and become a **performance** bottleneck while its read at the startup. Older logs are cleaned up periodically and doing **cleanup** operations on a single huge file is difficult to implement.

To handle this issue, Segmented Log can be used.

A single log is split into multiple segments. Log files are rolled after a specified size limit.

There needs to be an easy way to map logical log offsets (or log sequence numbers) to the log segment files. Then we may  easily tell which log entry stores in which log segment file.



* Each log segment file name is generated by some well known prefix and the base offset (or **start log entry number**).
* Each log entry number is divided into two parts, the **name** of the **file** and the **transaction offset**.

Zookeeper, Kafka, most databases follow log segmentation.


### Deduplication

The write ahead log is append-only. Because of this behavior, in case of client communication failure and **retries**, logs can contain **duplicate** entries.

When the log entries are applied, it needs to make sure that the duplicates are ignored. We may either use a HashMap as log storage or deduplicate based on the unique identifier of each request.


## *References

[https://www.postgresql.fastware.com/blog/back-to-basics-with-postgresql-memory-components#:~:text=WAL%20Buffers,data%20during%20database%20recovery%20operations](https://www.postgresql.fastware.com/blog/back-to-basics-with-postgresql-memory-components#:~:text=WAL%20Buffers,data%20during%20database%20recovery%20operations).

[https://severalnines.com/database-blog/architecture-and-tuning-memory-postgresql-databases#:~:text=Memory%20in%20PostgreSQL%20can%20be,processes%20of%20a%20PostgreSQL%20server](https://severalnines.com/database-blog/architecture-and-tuning-memory-postgresql-databases#:~:text=Memory%20in%20PostgreSQL%20can%20be,processes%20of%20a%20PostgreSQL%20server).

[https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html](https://martinfowler.com/articles/patterns-of-distributed-systems/wal.html)

[https://martinfowler.com/articles/patterns-of-distributed-systems/log-segmentation.html](https://martinfowler.com/articles/patterns-of-distributed-systems/log-segmentation.html)

[https://www.postgresql.org/docs/current/wal-intro.html#:~:text=Journaled%20file%20systems%20do%20improve,file%20changed%20by%20the%20transaction](https://www.postgresql.org/docs/current/wal-intro.html#:~:text=Journaled%20file%20systems%20do%20improve,file%20changed%20by%20the%20transaction).

[https://arctype.com/blog/postgres-ordbms-explainer/](https://arctype.com/blog/postgres-ordbms-explainer/)
