# Database Partitioning

<img width="853" alt="image" src="https://user-images.githubusercontent.com/47337188/208208406-2b95ab97-0c90-47ea-b961-ee131c46e02d.png">


As the figure shown above,

- a dataset can be partitioned. Each piece of data is assigned to one partition, and each 
partition can host many pieces of data.

- each partition is assigned to one node, and each node can handle multiple partitions.

- a read/write request against a piece of data should be forwarded to the node (and the partition) that hosts the 
data. 

There is physical partitioning and logical partitioning. Here, Database Partitioning is more about physical 
partitioning, since it affects how the data is stored.

Partitioning is necessary when you have so much data that storing and processing it on a single machine is no longer 
feasible. The **goal** of partitioning is to spread the data and query load evenly across multiple machines, avoiding 
hot spots (nodes with disproportionately high load). This requires choosing a partitioning **scheme** that is 
appropriate to your data, and **rebalancing** the partitions when nodes are added to or removed from the cluster.

## Approaches

### Key range partitioning
**where** keys are sorted, and a partition owns all the keys from some minimum up to some maximum. Sorting has the 
advantage that efficient range queries are possible, but there is a risk of hot spots if the application often 
accesses keys that are close together in the sorted order.

In this approach, partitions are typically rebalanced dynamically by splitting the range into two subranges when a 
partition gets too big.

### Hash partitioning
**where** a hash function is applied to each key, and a partition owns a range of hashes. This method destroys the 
ordering of keys, making range queries inefficient, but may distribute load more evenly.

When partitioning by hash, it is common to create a fixed number of partitions in advance, to assign several 
partitions to each node, and to move entire partitions from one node to another when nodes are added or removed. 
Dynamic partitioning can also be used.

## Rebalancing

Over time, things change in a database:

- The query throughput increases, so you want to add more CPUs to handle the load.

- The dataset size increases, so you want to add more disks and RAM to store it.

- A machine fails, and other machines need to take over the failed machine’s responsibilities.

All of these changes call for data and requests to be moved from one node to another. The process of moving load 
from one node in the cluster to another is called **rebalancing**.

No matter which partitioning scheme is used, rebalancing is usually expected to meet some minimum **requirements**:

- After rebalancing, the load (data storage, read and write requests) should be shared fairly between the nodes in 
the cluster.

- While rebalancing is happening, the database should continue accepting reads and writes.

- No more data than necessary should be moved between nodes, to make rebalancing fast and to minimize the network and 
disk I/O load.

### Fixed number of partitions

Fortunately, there is a fairly simple solution: create many more partitions than there are nodes, and assign several 
partitions to each node.

Now, if a node is added to the cluster, the new node can steal a few partitions from every existing node until 
partitions are fairly distributed once again, as shown below. If a node is removed from the cluster, the same 
happens in reverse.

![image](https://user-images.githubusercontent.com/47337188/208208606-7bdda57f-6034-4bc2-8832-b79c994e84b1.png)

Only entire partitions are moved between nodes. The number of partitions does not change, nor does the assignment of 
keys to partitions. The only thing that changes is the assignment of partitions to nodes.

### Dynamic partitioning

When a partition grows to exceed a configured size (on HBase, the default is 10 GB), it is split into two partitions 
so that approximately half of the data ends up on each side of the split. After a large partition has been split, 
one of its two halves can be transferred to another node in order to balance the load.

Conversely, if lots of data is deleted and a partition shrinks below some threshold, it can be merged with an 
adjacent partition.

### Partitioning proportionally to nodes

With dynamic partitioning, the number of partitions is proportional to the size of the dataset, since the splitting 
and merging processes keep the size of each partition between some fixed minimum and maximum.

On the other hand, with a fixed number of partitions, the size of each partition is proportional to the size of the 
dataset.

In both of these cases, the number of partitions is independent of the number of nodes.

A third option, used by Cassandra and Ketama, is to make the number of partitions proportional to the number of 
nodes—in other words, to have a fixed number of partitions per node.

When a new node joins the cluster, it randomly chooses a fixed number of existing partitions to split, and then 
takes ownership of one half of each of those split partitions while leaving the other half of each partition in place.

In this case, the size of each partition grows proportionally to the dataset size while the number of nodes remains 
unchanged, but when you increase the number of nodes, the partitions become smaller again.

## Request Routing

When a client wants to make a request, how does it know which node to connect to?

As partitions are rebalanced, the assignment of partitions to nodes changes. Somebody needs to stay on top of those 
changes in order to answer the question: if I want to read or write the key “foo”, which IP address and port number 
do I need to connect to?

This is an instance of a more general problem called service discovery, which isn’t limited to just databases. Any 
piece of software that is accessible over a network has this problem.

![image](https://user-images.githubusercontent.com/47337188/208208790-c11e01fa-96d8-4b3c-b9d1-fa47d3e5605f.png)

On a high level, there are a few different approaches to this problem, as shown above:

- Allow clients to contact any node (e.g., via a round-robin load balancer). If that node coincidentally owns the 
partition to which the request applies, it can handle the request directly; otherwise, it forwards the request to 
the appropriate node, receives the reply, and passes the reply along to the client.

- Send all requests from clients to a routing tier first, which determines the node that should handle each request 
and forwards it accordingly. This routing tier does not itself handle any requests; it only acts as a 
partition-aware load balancer.

- Require that clients be aware of the partitioning and the assignment of partitions to nodes. In this case, a client 
can connect directly to the appropriate node, without any intermediary.

In all cases, the key problem is: how does the component making the routing decision (which may be one of the nodes, 
or the routing tier, or the client) learn about changes in the assignment of partitions to nodes?

Many distributed data systems rely on a separate coordination service such as ZooKeeper to keep track of this 
cluster metadata. Each node registers itself in ZooKeeper, and ZooKeeper maintains the authoritative mapping of 
partitions to nodes. Other actors, such as the routing tier, can subscribe to this information in ZooKeeper. 
Whenever a partition changes ownership, or a node is added or removed, ZooKeeper notifies the routing tier so that 
it can keep its routing information up to date.

![image](https://user-images.githubusercontent.com/47337188/208208887-c8958ac4-a295-43f0-8324-1aef136af58f.png)

## References

Designing Data-Intensive Applications By Martin Kleppmann

