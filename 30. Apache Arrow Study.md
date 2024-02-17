# Apache Arrow Study

Apache Arrow is a columnar, in-memory, cross-language data layout format.

It is a building block for big data systems, focusing on efficient data transfers between machines in a cluster and between different big data systems.

## Table Storage -> Columnar -> Arrow

Many people model their data in a set of two-dimensional tables where each row corresponds to an entity, and each column an attribute about that entity.

However, storage is one-dimensional -- you can only read data sequentially from memory or disk in one dimension.

Therefore, there are two primary options for storing tables on storage:
- Store one row sequentially, followed by the next row, and then the next one, etc; 
- Store the first column sequentially, followed by the next column, and then the next one, etc.

Apache Arrow is a columnar data representation format that accelerates data analytics workloads.

On top of the format, Apache Arrow offers a set of libraries (including C, C++, C#, Go, Java, JavaScript, MATLAB, Python, R, Ruby, and Rust), to work with data in the Apache Arrow format.

## Data Transfer -> (De)serialization -> Zero-copy -> Arrow

Typically, a data transfer consists of:

- serializing data in a format
- sending the serialized data over a network connection
- deserializing the data on the receiving side

An example is as below:

<img width="533" alt="image" src="https://user-images.githubusercontent.com/47337188/181862322-b3ccb4af-e716-4f78-a2e9-9e9b4538ce9e.png">

In this process, there is one factor we control in software: (de)serialization.

Serialization converts the memory used by objects into a common format.

The format has a specification, and for each programming language and platform, a library is provided converting objects to serialized form and back.

When we are transferring lots of data, it will become a big bottleneck. Hence, can we eliminate the serialization process in those cases?

This is actually the goal of zero-copy serialization frameworks, such as Apache Arrow and FlatBuffers.

FlatBuffers uses a row-oriented format for its tables, Arrow uses a columnar format for storing tabular data. And that makes all the difference for analytical (OLAP) queries on big data sets.

Zero-copy refers here to the fact that the bytes your application works on can be transferred over the wire without any modification. Likewise, on the receiving end, the application can start working on the bytes as is, without a deserialization step.

Zero-copy also means if you have an Arrow table in C# you can map that memory to a different language and start processing on it without doing any kind of "language-to-language" marshaling of data. This zero-copy allows for efficient hand-off between languages.

<img width="542" alt="image" src="https://user-images.githubusercontent.com/47337188/181863362-c803c333-f92e-417d-b303-c8a0ced69ec3.png">

## Arrow + gRPC -> Apache Arrow Flight

Arrow Flight is a framework for transporting Arrow data efficiently over the network.

At a high level, Flight is a remote procedure call (RPC) framework.

RPC is a paradigm for structuring inter-process communications, whether it’s between two processes on the same machine or across the network. 

As the name implies, RPC models communication as calling remote functions and getting back results, just like in procedural programming — except the code being executed is in some other process.

Accordingly, Flight provides functions that fetch Arrow data from (or send data to) some remote process.

<img width="754" alt="image" src="https://user-images.githubusercontent.com/47337188/181865714-ef9c5ef4-cd60-4fb3-8025-7e157c8affaa.png">

Flight lets gRPC handle all the low-level details around network communications and layers its own optimizations and integration with Arrow data on top.

Protocol Buffers (“Protobuf”), a serialization format and library from Google, often fills that role for applications using gRPC, and it’s also used in Flight for metadata, alongside Arrow itself for data, of course.

### Protobuf <> Arrow
Protobuf is designed to create a common "on the wire" or "disk" format for data.
Arrow is designed to create a common "in memory" format for the data.

See https://stackoverflow.com/questions/66521194/comparison-of-protobuf-and-arrow.

## Arrow Use Case:
Fetching result sets over these clients now leverages the Arrow columnar format to avoid the overhead previously associated with serializing and deserializing Snowflake data structures which are also in columnar format.

If you work with Pandas DataFrames, the performance is even better with the introduction of our new Python APIs, which download result sets directly into a Pandas DataFrame. Internal tests show an improvement of up to 5x for fetching result sets over these clients, and up to a 10x improvement if you download directly into a Pandas DataFrame using the new Python client APIs.

See https://www.snowflake.com/blog/fetching-query-results-from-snowflake-just-got-a-lot-faster-with-apache-arrow/

## *References
[Overview of Serialization Technologies](https://indico.cern.ch/event/658060/contributions/2898569/attachments/1622526/2582399/pivarski-serialization.pdf)

https://arrow.apache.org/overview/

http://dbmsmusings.blogspot.com/2017/10/apache-arrow-vs-parquet-and-orc-do-we.html

https://www.infoq.com/articles/apache-arrow-java/

https://arrow.apache.org/blog/2019/10/13/introducing-arrow-flight/

