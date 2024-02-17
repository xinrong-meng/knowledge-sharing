# Storage and Retrieval

As an application developer, if you’re armed with this knowledge about the internals of storage engines, you are in a
much better position to know **which tool is best suited** for your particular application. If you need to adjust a
**database’s tuning** parameters, this understanding allows you to imagine what effect a higher or a lower value may have.

Although this chapter couldn’t make you an expert in tuning any one particular storage engine, it has hopefully
equipped you with enough **vocabulary and ideas** that you can make sense of the documentation for the database of your
choice.

In particular, there is a big difference between storage engines that are optimized for transactional workloads and 
those that are optimized for analytics.

## 1. Data Structures That Power Your Database

An index is an additional structure that is derived from the primary data. Many databases allow you to add and 
remove indexes, and this doesn’t affect the contents of the database; it only affects the performance of queries. 
Maintaining additional structures incurs overhead, especially on writes. For writes, it’s hard to beat the 
performance of simply appending to a file, because that’s the simplest possible write operation. Any kind of index 
usually slows down writes, because the index also needs to be updated every time data is written.

This is an important trade-off in storage systems: well-chosen indexes speed up read queries, but every index slows 
down writes. For this reason, databases don’t usually index everything by default, but require you—the application 
developer or database administrator—to choose indexes manually, using your knowledge of the application’s typical 
query patterns. You can then choose the indexes that give your application the greatest benefit, without introducing 
more overhead than necessary.

### 1.1 Hash Indexes

Let’s say our data storage consists only of appending to a file. Then the simplest possible indexing strategy is 
this: keep an in-memory hash map where every key is mapped to a byte offset in the data file—the location at which 
the value can be found.

This is essentially what Bitcask (the default storage engine in Riak) does.

#### Compaction and Merging

We only ever append to a file—so how do we avoid eventually running out of disk space?

A good solution is to break the log into **segments** of a certain size by closing a segment file when it reaches a 
certain size, and making subsequent writes to a new segment file. We can then perform **compaction** on these 
segments. Compaction means throwing away duplicate keys in the log, and keeping only the most recent update for each 
key.

Moreover, since compaction often makes segments much smaller, we can also **merge** several segments together at the 
same time as performing the compaction.

Segments are never modified after they have been written, so the merged 
segment is written to **a new file**. The merging and compaction of segments can be done in a **background thread**, 
and while it is going on, we can still continue to serve read requests using the old segment files, and write 
requests to the latest segment file. After the merging process is complete, we switch read requests to using the new 
merged segment instead of the old segments—and then the old segment files can simply be deleted.

Each segment now has its own in-memory hash table, mapping keys to file offsets. In order to find the value for a 
key, we first check the most recent segment’s hash map; if the key is not present we check the second-most-recent 
segment, and so on. The merging process keeps the number of segments small, so lookups don’t need to check many hash 
maps.

#### Real Implementations

Briefly, some of the issues that are important in a **real implementation** are:

- File format

CSV is not the best format for a log. It’s faster and simpler to use a **binary format** that first encodes the length 
of a string in bytes, followed by the raw string (without need for escaping).

- Deleting records

If you want to delete a key and its associated value, you have to append a **special deletion record** to the data file 
(sometimes called a tombstone). When log segments are merged, the tombstone tells the merging process to discard any 
previous values for the deleted key.

- Crash recovery

Bitcask speeds up recovery by storing a **snapshot** of each segment’s hash map on disk, which can be loaded into memory 
more quickly.

- Partially written records

The database may crash at any time, including halfway through appending a record to the log. Bitcask files include 
**checksums**, allowing such corrupted parts of the log to be detected and ignored.

- Concurrency control

As writes are appended to the log in a strictly sequential order, a common implementation choice is to have only **one** 
**writer thread**. Data file segments are append-only and otherwise immutable, so they can be **read concurrently** by 
multiple threads.

#### Pros and Cons

An append-only log seems wasteful at first glance: why don’t you update the file in place, overwriting the old value 
with the new value? But an append-only design turns out to be **good** for several reasons:

- Appending and segment merging are sequential write operations, which are generally much **faster** than random writes.

- **Concurrency and crash recovery** are much simpler if segment files are append-only or immutable. For example, you 
  don’t have to worry about the case where a crash happened while a value was being overwritten, leaving you with a 
  file containing part of the old and part of the new value spliced together.

However, the hash table index also has **limitations**:

- The hash table must **fit in memory**, so if you have a very large number of keys, you’re out of luck.
- **Range queries** are not efficient.

### 1.2 SSTables and LSM-Trees

Now we can make a simple change to the format of our segment files: we require that the sequence of key-value pairs 
is sorted by key. We call this format **Sorted String Table**, or SSTable for short.

SSTables have several big advantages over log segments with hash indexes:

- Merging segments is simple and efficient, even if the files are bigger than the available memory.
- In order to find a particular key in the file, you no longer need to keep an index of all the keys in memory. You 
  still need an in-memory index to tell you the offsets for some of the keys, but it can be sparse.
- Since read requests need to scan over several key-value pairs in the requested range anyway, it is possible to 
  group those records into a block and compress it before writing it to disk.

![image](https://user-images.githubusercontent.com/47337188/222936278-f3957cbb-8b38-4ff4-bd1b-fb47a9e81dd0.png)

#### LSM-tree: Constructing and maintaining SSTables

A LSM-tree is a data structure with performance characteristics that make it attractive for providing **indexed access** 
to **files** with high insert volume.

LSM-tree consists of some **memory** components and some disk components. Basically SSTable is just a one implemention 
of **disk** component for LSM-tree.

Maintaining a sorted structure on disk is possible (see “B-Trees”), but maintaining it **in memory** is much easier. 
There are plenty of well-known **tree** data structures that you can use, such as red-black trees or AVL trees. With 
these data structures, you can insert keys in any order and read them back in sorted order.

We can now make our storage engine work as follows:

- When a write comes in, add it to an **in-memory** balanced tree data structure
- When the memtable gets bigger than some threshold—typically a few megabytes—write it out **to disk** as an SSTable file.
- In order to serve a read request, first try to find the key in the memtable, then in the most recent on-disk 
  segment, then in the next-older segment, etc.
- From time to time, run a **merging** and **compaction** process in the background to combine segment files and to discard 
  overwritten or deleted values.

### 1.3 B-Trees

A B-tree is a self-balancing tree data structure that maintains sorted data and allows searches, sequential access, 
insertions, and deletions in logarithmic time. The B-tree generalizes the binary search tree, allowing for nodes 
with more than two children. Unlike other self-balancing binary search trees, the B-tree is well suited for 
storage systems that read and write relatively large blocks of data, such as databases and file systems.

B-trees break the database down into fixed-size blocks or **pages**, traditionally 4 KB in size (sometimes bigger), and 
read or write one page at a time. This design corresponds more closely to the underlying **hardware**, as disks are also 
arranged in fixed-size blocks.

Each page can be identified using an address or location, as shown below, which allows one page to refer to 
another—similar to a **pointer**, but **on disk** instead of in memory. We can use these page references to 
construct a tree of pages.

![image](https://user-images.githubusercontent.com/47337188/223282912-a0c1eb5a-f98d-497d-9f6d-e9e455ac4c19.png)

One page is designated as the root of the B-tree; whenever you want to look up a key in the index, you start here. 
The page contains several keys and references to child pages. Each child is responsible for a continuous range of 
keys, and the keys between the references indicate where the boundaries between those ranges lie.

## References

Designing Data-Intensive Applications By Martin Kleppmann

https://en.wikipedia.org/wiki/Log-structured_merge-tree

https://stackoverflow.com/questions/58168809/what-is-the-differences-between-the-term-sstable-and-lsm-tree

https://en.wikipedia.org/wiki/B-tree
