# Distributed Transactions and Consensus

Even if we capture the **causal ordering** (for example using Lamport timestamps), we saw that some things cannot be 
implemented this way: ensuring that a username is unique and rejecting concurrent registrations for the same username.
If one node is going to accept a registration, it needs to somehow know that another node isn’t concurrently in the
process of registering the same name. This problem led us toward **consensus**.

Achieving consensus in distributed computing means deciding something in such a way that **all nodes agree** on what was 
decided, and such that the decision is **irrevocable**.

Once you have an implementation of consensus, applications can use it for various purposes. For example, say you
have a database with single-leader replication. If the leader dies and you need to fail over to another node, the
remaining database nodes can use consensus to **elect a new leader**.

## Atomic Commit and Two-Phase Commit (2PC)

The outcome of a **transaction** is either a successful **commit**, in which case all of the transaction’s writes are 
made durable, or an **abort**, in which case all of the transaction’s writes are rolled back.

If some nodes commit the transaction but others abort it, the nodes become inconsistent with each other and the 
commit is **not atomic**. Once a transaction has been committed on one node, it cannot be retracted again if it later 
turns out that it was aborted on another node. For this reason, a node must only commit once it is certain that all 
other nodes in the transaction are also going to commit.

A **transaction commit** must be **irrevocable** — you are not allowed to change your mind and abort a 
transaction after it has been committed. The reason for this rule is that once data has been committed, it becomes 
visible to other transactions, and thus other clients may start relying on that data.

**Two-phase commit** is an algorithm for achieving **atomic transaction commit** across multiple nodes — i.e., to ensure that
either all nodes commit or all nodes abort.

Instead of a single commit request, as with a single-node transaction, the **commit/abort process** in 2PC is split into
**two phases** (hence the name).

![image](https://user-images.githubusercontent.com/47337188/213899762-dfc3b4f1-df9b-4137-8d83-202c0b8a25c4.png)

When 2PC is used, a distributed transaction begins with the application reading and writing data on multiple
database nodes, as normal. We call these database nodes **participants** in the transaction. Consider a transaction **coordinator** that manages the commits to database stores.
When the application is ready to commit, the coordinator begins **phase 1**: it sends a **prepare** request to each of the nodes, asking them
whether they are able to commit. The coordinator then tracks the responses from the participants:
- If all participants reply “yes,” indicating they are ready to commit, then the coordinator sends out a **commit**
  request in **phase 2**, and the commit actually takes place.
- If any of the participants replies “no,” the coordinator sends an **abort** request to all nodes in **phase 2**.

Thus, the protocol contains **two crucial “points of no return”**: **when a participant votes “yes,”** it promises that it
will definitely be able to commit later (although the coordinator may still choose to abort); and **once the
coordinator decides**, that decision is irrevocable. Those promises ensure the **atomicity** of 2PC.

### Coordinator failure
Without hearing from the coordinator, the participant has no way of knowing whether to commit or abort. In principle,
the participants could communicate among themselves to find out how each participant voted and come to some 
agreement, but that is not part of the 2PC protocol.

The only way 2PC can complete is by **waiting** for the coordinator to recover. This is why the coordinator must write 
its commit or abort decision to a **transaction log on disk** before sending commit or abort requests to participants: 
when the coordinator recovers, it determines the status of all in-doubt transactions by reading its transaction log. 
Thus, the commit point of 2PC comes down to a regular single-node atomic commit on the coordinator.

## Fault-Tolerant Consensus

The consensus problem is normally formalized as follows: one or more nodes may **propose** values, and the consensus 
algorithm **decides** on one of those values. In the seat-booking example, when several customers are concurrently 
trying to buy the last seat, each node handling a customer request may propose the ID of the customer it is serving, 
and the decision indicates which one of those customers got the seat.

A consensus algorithm must satisfy the following properties:

- Uniform agreement : No two nodes decide differently.

- Integrity : No node decides twice.

- Validity : If a node decides value v, then v was proposed by some node.

- Termination : Every node that does not crash eventually decides some value.

The **uniform** agreement and **integrity** properties define the core idea of consensus: everyone decides on the same 
outcome, and once you have decided, you cannot change your mind. The **validity** property exists mostly to rule out 
trivial solutions: for example, you could have an algorithm that always decides null, no matter what was proposed; 
this algorithm would satisfy the agreement and integrity properties, but not the validity property.

If you **don’t care about fault tolerance**, then satisfying the first three properties is easy: you can just hardcode 
one node to be the “dictator,” and let that node make all of the decisions. However, if that one node fails, then 
the system can no longer make any decisions. This is, in fact, what we saw in the case of **two-phase commit**: if the 
coordinator fails, in-doubt participants cannot decide whether to commit or abort.

The termination property formalizes the idea of fault tolerance. It essentially says that a consensus algorithm 
cannot simply sit around and do nothing forever—in other words, it must make progress. Even if some nodes fail, the 
other nodes must still reach a decision.

The best-known fault-tolerant consensus algorithms are Viewstamped Replication (VSR), Paxos, Raft, and Zab.

## Membership and Coordination Services

Projects like ZooKeeper or etcd are often described as “distributed key-value stores” or “coordination and 
configuration services.” The API of such a service looks pretty much like that of a **database**: you can read and write 
the value for a given key, and iterate over keys. So if they’re basically databases, why do they go to all the 
effort of **implementing a consensus algorithm**? What makes them different from any other kind of database?

ZooKeeper and etcd are designed to hold small amounts of data that can fit entirely in memory (although they still 
write to disk for durability)—so you wouldn’t want to store all of your application’s data here. That small amount 
of data is replicated across all the nodes using a fault-tolerant total order broadcast algorithm.

**1. Allocating work to nodes**

One example in which the ZooKeeper/Chubby model works well is if you have several instances of a process or service, 
and one of them needs to be chosen as leader or primary. If the leader fails, one of the other nodes should take 
over. This is of course useful for single-leader databases, but it’s also useful for job schedulers and similar 
stateful systems.

Another example arises when you have some partitioned resource (database, message streams, file storage, distributed 
actor system, etc.) and need to decide which partition to assign to which node. As new nodes join the cluster, some 
of the partitions need to be moved from existing nodes to the new nodes in order to rebalance the loads. As nodes 
are removed or fail, other nodes need to take over the failed nodes’ work.

These kinds of tasks can be achieved by ZooKeeper. If done correctly, this approach allows the application to 
automatically recover from faults without human intervention.

Normally, the kind of data managed by ZooKeeper is quite slow-changing: it represents information like “the node 
running on IP address 10.1.1.23 is the leader for partition 7,” and such assignments usually change on a timescale 
of minutes or hours. ZooKeeper is not intended for storing the runtime state of the application, which may change 
thousands or even millions of times per second. If application state needs to be replicated from one node to another,
other tools (such as Apache BookKeeper) can be used.

**2. Membership services**

ZooKeeper and friends can be seen as part of a long history of research into membership services. A membership 
service determines **which nodes** are currently **active** and live members of a cluster.

Due to unbounded network delays it’s **not possible** to reliably **detect** whether another node has failed.

However, if you couple failure detection with consensus, nodes can come to an **agreement** about which nodes should be 
considered alive or not.

It could still happen that a node is incorrectly declared dead by consensus, even though it is actually alive. But 
it is nevertheless very useful for a system to have agreement on which nodes constitute the current membership. For 
example, choosing a leader could mean simply choosing the lowest-numbered among the current members, but this 
approach would not work if different nodes have divergent opinions on who the current members are.

## Summary

This chapter referenced a large body of research on the theory of distributed systems. Although the theoretical 
papers and proofs are not always easy to understand, and sometimes make unrealistic assumptions, they are incredibly 
valuable for informing practical work in this field: they help us **reason about what can and cannot be done**, and help 
us find the counterintuitive **ways** in which **distributed systems** are often **flawed**.

## References

Designing Data-Intensive Applications By Martin Kleppmann