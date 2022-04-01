# Intro to MapReduce

MapReduce is a programming model and an associated implementation for processing big data.


## Programming model

**Map**, written by the user, takes an input pair and produces a set of intermediate key/value pairs. The MapReduce library groups together all intermediate values associated with the same intermediate key and passes them to the Reduce function.

The **Reduce** function, also written by the user, accepts an intermediate key and a set of values for that key. It merges together these values. Typically just zero or one output value is produced per Reduce invocation.

The intermediate values are supplied to the user’s reduce function via an **iterator**. This allows us to handle lists of values that are too large to fit in memory.


### Example: Word Count

Consider the problem of counting the number of occurrences of each word in a large collection of documents.


```
map(String key, String value):
  // key: document name; value: document contents
  for each word w in value:
    EmitIntermediate(w, "1");

reduce(String key, Iterator values):
    // key: a word, values: a list of counts
    int result = 0;
    for each v in values:
        result += ParseInt(v);
    Emit(AsString(result))
```


The map and reduce functions have associated types:

![alt_text](https://user-images.githubusercontent.com/47337188/161353474-b6cf8f34-0bbd-42e0-aefa-86d6d6d2b438.png "image_tooltip")



## Implementation

Many different implementations of the MapReduce interface are possible.

Here we look at Google’s.


### Execution

![alt_text](https://user-images.githubusercontent.com/47337188/161353485-c43a1ca9-b1c1-4546-b0b0-b2b45d8f5cd3.png "image_tooltip")


1. The MapReduce library in the user program first splits the input files into M(=5) pieces. It then starts up many copies of the program on a cluster of machines.

2. One of the copies of the program is special – the master. The rest are workers that are assigned work by the master. There are M map tasks and R reduce tasks to assign. The master picks idle workers and assigns each one a map task or a reduce task.

3. A worker who is assigned a map task reads the contents of the corresponding input split. It parses key/value pairs out of the input data and passes each pair to the user-defined Map function. The intermediate key/value pairs produced by the Map function are buffered in memory.

4. Periodically, the buffered pairs are written to local disk, partitioned into R regions by the partitioning function. The **locations** of these buffered pairs on the local disk are passed back to the master, who is responsible for forwarding these locations to the reduce workers.

5. When a reduce worker is notified by the master about these locations, it uses remote procedure calls to read the buffered data from the local disks of the map workers. When a reduce worker has read all intermediate data, it sorts it by the intermediate keys
so that all occurrences of the same key are grouped together. The sorting is needed because typically many different keys map to the same reduce task. If the amount of intermediate data is too large to fit in memory, an external sort is used.

6. The reduce worker iterates over the sorted intermediate data and for each unique intermediate key encountered, it passes the key and the corresponding set of intermediate values to the user’s Reduce function. The output of the Reduce function is appended
to a final output file for this reduce partition.


### Fault Tolerance - Worker Failure

The master pings every worker periodically. If no response is received from a worker in a certain amount of time, the master marks the worker as failed.

Completed map tasks are re-executed on a failure because their output is stored on the local disk(s) of the failed machine and is therefore inaccessible. Completed reduce tasks do not need to be re-executed since their output is stored in a global file system.


### Locality

Network bandwidth is conserved by taking advantage of the fact that the **input** data (managed by GFS) is stored on the **local disks of the machines that make up our cluster**. GFS divides each file into 64 MB blocks, and stores several copies of each block (typically 3 copies) on different machines.

The MapReduce master takes the location information of the input files into account and attempts to schedule a map task on a machine that **contains** a replica of the corresponding input data. Failing that, it attempts to schedule a map task **near** a replica of that task’s input data (e.g., on a worker machine that is on the same network switch as the machine containing the data).


## Limitations



* MapReduce is great at one-pass computation, but inefficient for multi-pass algorithms


![alt_text](https://user-images.githubusercontent.com/47337188/161353491-3a16b46f-b72b-47ed-98f3-73c1f40d07da.png "image_tooltip")




* No efficient primitives for data sharing
    * State between steps goes to a distributed file system
    * Slow due to replication & disk storage.

Commonly spend 90% of time doing I/O.


## *References

[https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf](https://static.googleusercontent.com/media/research.google.com/en//archive/mapreduce-osdi04.pdf)

[https://stanford.edu/~rezab/classes/cme323/S18/notes/Intro_Spark.pdf](https://stanford.edu/~rezab/classes/cme323/S18/notes/Intro_Spark.pdf)
