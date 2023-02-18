# Consistency

We know that the system stores the most recently updated data on a single computer. However, data is shared and 
replicated across many computing nodes in a distributed system.

Consistency is a property of the distributed system which ensures that every node or replica has the same view of 
data at a given time, irrespective of which client has updated the data.

## Consistency Models

There is some similarity between **distributed consistency models** and the hierarchy of **transaction isolation levels** we 
discussed previously. But while there is some overlap, they are mostly independent concerns: transaction isolation is
primarily about **avoiding race conditions due to concurrently executing transactions**, whereas distributed consistency 
is mostly about coordinating **the state of replicas in the face of delays and faults**.

### 1. Eventual Consistency

Most replicated databases provide at least eventual consistency, which means that if you **stop writing** to the 
database and **wait for some unspecified length of time**, then eventually all **read** requests will return the **same** value. 
better name for eventual consistency may be **convergence**, as we expect all replicas to eventually converge to the 
same value.

Eventual consistency is **hard for application developers** because it is so different from the behavior of variables in 
a normal single-threaded program. When working with a database that provides only weak guarantees, you need to be 
constantly aware of its limitations and not accidentally assume too much.

### 2. Linearizability
It is also known as atomic consistency, **strong consistency**, immediate consistency, or external consistency.

The basic idea is to make a system appear as if there were **only one copy of the data**, and all **operations** on it are 
**atomic**. With this guarantee, even though there may be multiple replicas in reality, the **application does not** 
need to **worry** about them.

![image](https://user-images.githubusercontent.com/47337188/208594082-9ebdc72d-1178-4bae-8ee7-1b7efcdc2f08.png)

As shown above, after any one read has returned the new value, all following reads (on the same or other clients) 
must also return the new value. In a linearizable system we imagine that there must be some point in time (between 
the start and end of the write operation) at which the value of x **atomically flips** from 0 to 1. Thus, if one 
client’s read returns the new value 1, all subsequent reads must also return the new value, even if the write 
operation has not yet completed.

#### 2.1 Use Cases

- **Locking and leader election**

A system that uses single-leader replication needs to ensure that there is indeed only one leader, not several 
(split brain). One way of electing a leader is to use a **lock**: every node that starts up tries to acquire the lock, 
and the one that succeeds becomes the leader. No matter how this lock is implemented, it must be linearizable: all 
nodes must agree which node owns the lock; otherwise it is useless.

- **Constraints and uniqueness guarantees**

Uniqueness constraints are common in databases: for example, a username or email address must uniquely identify one 
user, and in a file storage service there cannot be two files with the same path and filename. If you want to 
enforce this constraint **as the data is written** (such that if two people try to concurrently create a user or a file 
with the same name, one of them will be returned an error), you need linearizability.

Similar issues arise if you want to ensure that a bank account balance never goes negative, or that you don’t sell 
more items than you have in stock in the warehouse, or that two people don’t concurrently book the same seat on a 
flight or in a theater. These constraints all require there to be **a single up-to-date value** (the account balance, 
the stock level, the seat occupancy) that all nodes agree on.

#### 2.2 Implementation

The simplest implementation is to really **only use a single copy of the data**. However, that approach would not be able 
to **tolerate faults**: if the node holding that one copy failed, the data would be lost, or at least inaccessible until 
the node was brought up again.

Let’s revisit the replication methods, and compare whether they can be made linearizable:

- Single-leader replication (potentially linearizable)
- Consensus algorithms (linearizable)
- Multi-leader replication (not linearizable)
- Leaderless replication (probably not linearizable)

### 3. Causal Consistency

Causal consistency is a weak form of consistency that preserves the order of causally related operations. A 
**happens-before relationship** between operations captures **causality**. This means all processes must see potentially 
causally related operations in the same order.

In other words, if a happens before b, then a must execute before b on all replicas. All other concurrent operations 
may be seen in different orders.

Unlike linearizability, which puts all operations in a **single, totally ordered timeline**, causality provides us with 
a weaker consistency model: some things can be concurrent, so the version history is like a timeline with **branching** 
**and merging**.

**Linearizability implies causality**: any system that is linearizable will preserve causality correctly. 
Linearizability is not the only way of preserving causality—there are other ways too.

#### 3.1 Happens-before Relationship

An event is something happening at a server node (sending or receiving messages, or a local execution step). If an 
event a happens before b, we write it as `a -> b`.

There are three conditions in which we can say an event a happens before b:

- If it is the same node and a occurs before b, then `a -> b`
- If c is a message receipt of b, then `b -> c`
- Transitivity: If `a -> b` and `b -> c`, then `a -> c`

The following diagram illustrates the happens-before relation:

![image](https://user-images.githubusercontent.com/47337188/215233519-08b76eed-26fe-4030-b87e-a3d9e31e3884.png)

A happens-before relation does not order all events. For instance, the events a and d are not related by `->`. Hence, they are **concurrent**.

**Lamport clocks** represent time logically in a distributed system. They are also known as logical clocks. The idea 
behind Lamport clocks is to disregard physical time and **capture** just a “happens-before” relationship between a pair 
of events.

Lamport clocks tag events in a distributed system and order them accordingly. We seek a clock time `C(a)` for every 
event `a`. The clock condition is defined as follows: If `a -> b`, then `C(a) < C(b)`.

Each process maintains an event counter. This event counter is the **local** Lamport clock.

The Lamport clock algorithm works in the following way:

- Before the execution of an event, the local clock is updated. This can be explained by the equation `Ci = Ci+1`, 
where i is the process identifier.
- When a message is sent to another process, the message contains the process’ local clock, `Cm`.
- When a process receives a message `m`, it sets its local clock to `1+max(CI, Cm)`.

The following diagram illustrates how the Lamport clock algorithm works:

![image](https://user-images.githubusercontent.com/47337188/215233443-810ae7c6-af30-4440-883c-d703098b3343.png)

#### 3.2 Example

In the following example, we have a distributed system consisting of four different processes: P1, P2, P3, and P4.

![image](https://user-images.githubusercontent.com/47337188/215233557-35de5afe-add6-4a29-aadc-bdcdc5b1d522.png)

There are a number of operations happening at every process. W(Y,A) means that the value of object Y is being written as A. R(Y) means that the value of object Y is being read.

At first glance, the following sequence of operations might seem causally consistent, but they are not.

Having read C, P3 must continue to read C or some newer value (perhaps B), but can’t go back to A. That’s because W(Y,C) was conditional upon W(Y,A) having finished.

If P3 had read B on its second read, we could say that this system guaranteed causal consistency. That’s because W(Y,B) and W(Y,C) are not causally related. Instead, they are concurrent.

## References

Designing Data-Intensive Applications By Martin Kleppmann

https://www.educative.io/answers/what-is-causal-consistency-in-distributed-systems

https://www.educative.io/answers/what-are-lamport-clocks
