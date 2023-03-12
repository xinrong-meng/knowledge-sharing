# Storage and Retrieval

## 1. Transaction Processing or Analytics?

Comparing characteristics of transaction processing versus analytic systems:

![image](https://user-images.githubusercontent.com/47337188/224457842-4e432cb0-8323-43c4-870c-b23401cea1bf.png)

At first, the same databases were used for both transaction processing and analytic queries. SQL turned out to be 
quite flexible in this regard: it works well for OLTP-type queries as well as OLAP-type queries. Nevertheless, in 
the late 1980s and early 1990s, there was a trend for companies to stop using their OLTP systems for analytics purposes, and to run the analytics on a separate database instead. This separate database was called a data warehouse.

### Data Warehousing

The data warehouse contains a read-only copy of the data in all the various OLTP systems in the company. Data is 
extracted from OLTP databases (using either a periodic data dump or a continuous stream of updates), transformed 
into an analysis-friendly schema, cleaned up, and then loaded into the data warehouse. This process of getting data 
into the warehouse is known as Extract–Transform–Load (ETL) and is illustrated as below.

![image](https://user-images.githubusercontent.com/47337188/224458015-6a4c4499-c33b-444a-a204-b5b5556c7626.png)

A big advantage of using a separate data warehouse, rather than querying OLTP systems directly for analytics, is 
that the data warehouse can be optimized for analytic access patterns.

When your queries require sequentially scanning across a large number of rows, indexes are much less relevant.
Instead it becomes important to encode data very compactly, to minimize the amount of data that the query needs to
read from disk. We will see how column-oriented storage helps achieve this goal.

## 2. Column-Oriented Storage

Although fact tables are often over 100 columns wide, a typical data warehouse query only accesses 4 or 5 of them at 
one time ("SELECT *" queries are rarely needed for analytics). An example is shown as below

```sql
-- Analyzing whether people are more inclined to buy fresh fruit or candy, depending on the day of the week
SELECT
  dim_date.weekday, dim_product.category,
  SUM(fact_sales.quantity) AS quantity_sold
FROM fact_sales
  JOIN dim_date    ON fact_sales.date_key   = dim_date.date_key
  JOIN dim_product ON fact_sales.product_sk = dim_product.product_sk
WHERE
  dim_date.year = 2013 AND
  dim_product.category IN ('Fresh fruit', 'Candy')
GROUP BY
  dim_date.weekday, dim_product.category;
```

In most OLTP databases, storage is laid out in a **row-oriented** fashion: all the values from one row of a table are 
stored next to each other. Document databases are similar: an entire document is typically stored as one contiguous 
sequence of bytes.

The idea behind column-oriented storage is simple: don’t store all the values from one row together, but store all 
the values from each column together instead. If each column is stored in a separate file, a query only needs to 
read and parse those columns that are used in that query, which can save a lot of work.

Column storage is easiest to understand in a relational data model as shown below, but it applies equally to 
nonrelational data.

![image](https://user-images.githubusercontent.com/47337188/224458378-bb8a8185-1590-48d1-a141-ea74d4bf22ec.png)

The column-oriented storage layout relies on each column file containing the rows in the same order. Thus, if you 
need to reassemble an entire row, you can take the 23rd entry from each of the individual column files and put them 
together to form the 23rd row of the table.

### 2.1 Column Compression

Besides only loading those columns from disk that are required for a query, we can further reduce the demands on 
disk throughput by compressing data.

Often, the number of distinct values in a column is small compared to the number of rows. 

We can now take a column with n distinct values and turn it into n separate bitmaps: one bitmap for each distinct 
value, with one bit for each row. The bit is 1 if the row has that value, and 0 if not. An example is as shown below.

![image](https://user-images.githubusercontent.com/47337188/224458752-99085d28-81e3-4dd8-943b-974c20bcb511.png)

If n is very small (for example, a country column may have approximately 200 distinct values), those bitmaps can be 
stored with one bit per row. But if n is bigger, there will be a lot of zeros in most of the bitmaps (we say that 
they are sparse). In that case, the bitmaps can additionally be run-length encoded, as shown above.

Bitmap indexes such as these are very well suited for the kinds of queries that are common in a data warehouse. Two 
examples are as shown below:

a)
```sql
WHERE product_sk IN (30, 68, 69)
```
Load the three bitmaps for product_sk = 30, product_sk = 68, and product_sk = 69, and calculate the bitwise OR of 
the three bitmaps, which can be done very efficiently.

b)
```sql
WHERE product_sk = 31 AND store_sk = 3:
```
Load the bitmaps for product_sk = 31 and store_sk = 3, and calculate the bitwise AND. This works because the columns contain the rows in the same order, so the kth bit in one column’s bitmap corresponds to the same row as the kth bit in another column’s bitmap.

### 2.2 Sort Order in Column Storage

In a column store, it doesn’t necessarily matter in which order the rows are stored. It’s easiest to store them in 
the order in which they were inserted, since then inserting a new row just means appending to each of the column 
files. However, we can choose to impose an order, like we did with SSTables previously, and use that as an indexing 
mechanism.

Note that it wouldn’t make sense to sort each column independently, because then we would no longer know which items 
in the columns belong to the same row. We can only reconstruct a row because we know that the kth item in one column 
belongs to the same row as the kth item in another column.

Rather, the data needs to be sorted an entire row at a time, even though it is stored by column. The administrator 
of the database can choose the columns by which the table should be sorted, using their knowledge of common queries. 
For example, if queries often target date ranges, such as the last month, it might make sense to make date_key the 
first sort key. Then the query optimizer can scan only the rows from the last month, which will be much faster than 
scanning all rows.

A second column can determine the sort order of any rows that have the same value in the first column. For example, 
if date_key is the first sort key in Figure 3-10, it might make sense for product_sk to be the second sort key so 
that all sales for the same product on the same day are grouped together in storage. That will help queries that 
need to group or filter sales by product within a certain date range.

Another advantage of sorted order is that it can help with compression of columns. If the primary sort column does 
not have many distinct values, then after sorting, it will have long sequences where the same value is repeated many 
times in a row. A simple run-length encoding, like we used for the bitmaps in the previous example could compress that 
column down to a few kilobytes—even if the table has billions of rows.

### 2.3 Writing to Column-Oriented Storage

An update-in-place approach, like **B-trees** use, is not possible with compressed columns. If you wanted to insert a 
row in the middle of a sorted table, you would most likely have to rewrite all the column files. As rows are 
identified by their position within a column, the insertion has to update all columns consistently.

Fortunately, we have already seen a good solution earlier in this chapter: **LSM-trees**. All writes first go to an 
in-memory store, where they are added to a sorted structure and prepared for writing to disk. It doesn’t matter 
whether the in-memory store is row-oriented or column-oriented. When enough writes have accumulated, they are merged 
with the column files on disk and written to new files in bulk.

Queries need to examine both the column data on disk and the recent writes in memory, and combine the two. However, 
the query optimizer hides this distinction from the user.

### 2.4 Aggregation: Data Cubes and Materialized Views

Another aspect of data warehouses that is worth mentioning briefly is **materialized aggregates**. As discussed earlier, 
data warehouse queries often involve an aggregate function, such as COUNT, SUM, AVG, MIN, or MAX in SQL. If the same 
aggregates are used by many different queries, it can be wasteful to crunch through the raw data every time. Why not 
**cache** some of the counts or sums that queries use most often? One way of creating such a cache is a materialized 
view.

In a relational data model, it is often defined like a standard (virtual) view: a table-like object whose contents 
are the results of some query. The difference is that a materialized view is an **actual copy of the query results**, 
written to **disk**, whereas a virtual view is just a shortcut for writing queries.

When the underlying data changes, a materialized view needs to be updated, because it is a denormalized copy of the 
data. The database can do that automatically, but such updates make writes more expensive, which is why materialized 
views are not often used in OLTP databases.

A common special case of a materialized view is known as a data cube or OLAP cube. It is a grid of aggregates 
grouped by different dimensions.

## 3. Summary

OLTP systems are typically user-facing, which means that they may see a huge volume of requests. In order to handle 
the load, applications usually only touch a small number of records in each query. The application requests records 
using some kind of key, and the storage engine uses an index to find the data for the requested key. Disk seek time 
is often the bottleneck here.

Data warehouses and similar analytic systems are less well known, because they are primarily used by business 
analysts, not by end users. They handle a much lower volume of queries than OLTP systems, but each query is 
typically very demanding, requiring many millions of records to be scanned in a short time. Disk bandwidth (not seek 
time) is often the bottleneck here, and column-oriented storage is an increasingly popular solution for this kind of 
workload.

On the OLTP side, we saw storage engines from two main schools of thought:

- The log-structured school, which only permits appending to files and deleting obsolete files, but never updates a 
file that has been written. Bitcask, SSTables, LSM-trees, LevelDB, Cassandra, HBase, Lucene, and others belong to 
this group.

- The update-in-place school, which treats the disk as a set of fixed-size pages that can be overwritten. B-trees are 
the biggest example of this philosophy, being used in all major relational databases and also many nonrelational ones.

(Again.) As an application developer, if you’re armed with this knowledge about the internals of storage engines, you 
are in a much better position to know which tool is best suited for your particular application. If you need to adjust a 
database’s tuning parameters, this understanding allows you to imagine what effect a higher or a lower value may have.

## References

Designing Data-Intensive Applications By Martin Kleppmann
