# Columnar Data Formats

Columnar data structures provide a number of performance advantages over traditional row-oriented data structures for analytics. 

These include benefits for data **on disk** – fewer disk seeks, more effective compression, faster scan rates – as well as more efficient use of CPU for data **in memory**.  

## On disk: e.g. Parquet
![image](https://user-images.githubusercontent.com/47337188/179433609-47f1c664-18dd-4973-9ad4-112e898866fe.png)

Most systems are engineered to minimize the number of disk seeks and the amount of data scanned, as these operations can add tremendous latency. 

In **transactional workloads**, as data is written to a table in a row-oriented database, the columns for a given row are written out to disk contiguously, which is very efficient for writes. 

**Analytical workloads** differ in that most queries read a small subset of the columns for large numbers of rows at a time. 

In a traditional row-oriented database, the system might perform a seek for each row, and most of the columns would be read from disk into memory unnecessarily.
A columnar database organizes the values for a given column contiguously on disk. This has the advantage of significantly reducing the number of seeks for multi-row reads. 

Furthermore, compression algorithms tend to be much more effective on a single data type rather than the mix of types present in a typical row. 

The tradeoff is that writes are slower, but this is a good optimization for analytics where reads typically far outnumber writes.

## In memory: e.g. Arrow

In-memory columnar data has bottlenecks as below.

**Bottleneck: CPU throughput**

Because reading data from memory is thousands of times faster than reading data from disk, there is enormous interest in the data world in how to make optimal use of RAM for analytics.

The trade-offs being for columnar data are different for in-memory from on-disk. 

- For data on disk, usually IO dominates latency, which can be addressed with aggressive compression, at the cost of CPU. 
- In memory, access is much faster and we want to optimize for **CPU throughput** by paying attention to cache locality, pipelining, and SIMD instructions.

One of the funny things about computer science is that while there is a common set of resources – RAM, CPU, storage, network – each language has an entirely different way of interacting with those resources. 

**Bottleneck: handoffs**

When different programs need to interact – within and across languages – there are inefficiencies in the handoffs that can dominate the overall cost.

We viewed these handoffs as the next obvious bottleneck for in-memory processing.

Here Arrow comes to the stage. We will have a separate session to discuss Apache Arrow.

![image](https://user-images.githubusercontent.com/47337188/179433791-01df26d9-4c62-4d15-ad4e-f756fc14b526.png)

## Parquet and Arrow

Since both are columnar we can implement efficient vectorized converters from one to the other. 

Pandas is a good example of using both projects.

Users can save a Pandas data frame to Parquet and read a Parquet file to in-memory Arrow.

Pandas can also directly work on top of Arrow columns, paving the way for a faster Spark integration.

## Case study: Pandas integration with Arrow
The equivalent to a pandas DataFrame in Arrow is a Table. Both consist of a set of named columns of equal length.

While pandas only supports flat columns, the Table also provides nested columns, thus it can represent more data than a DataFrame, so a full conversion is not always possible.

```
>>> import pyarrow as pa
>>> import pandas as pd
>>> df = pd.DataFrame({"a": [1, 2, 3]})
>>> df
   a
0  1
1  2
2  3
>>> table = pa.Table.from_pandas(df)
>>> table
pyarrow.Table
a: int64
>>> df_new = table.to_pandas()
>>> df_new
   a
0  1
1  2
2  3

```


## *References
https://www.kdnuggets.com/2017/02/apache-arrow-parquet-columnar-data.html
