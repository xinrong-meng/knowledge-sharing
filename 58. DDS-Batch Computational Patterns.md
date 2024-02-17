# Batch Computational Patterns

In contrast to long-running applications, batch processes are expected to only run for a short period of time. Batch 
processes are generally characterized by the need to process large amounts of data quickly using parallelism to 
speed up the processing.

## Work Queue Systems

The simplest form of batch processing is a work queue. 

<img width="631" alt="image" src="https://user-images.githubusercontent.com/47337188/243146235-6a0099e2-4fa3-4652-a917-d0b393b9a1b2.png">

In a work queue system, there is a batch of work to be performed. Each piece of work is wholly **independent** of the 
other and can be processed without any interactions.

## Event-Driven Batch Processing

Work queues are great for enabling individual transformations of one input to one output. However, there are a 
number of batch applications where you want to perform more than a single action, or you may need to generate 
multiple different outputs from a single data input. In these cases, you start to link work queues together so that 
the output of one work queue becomes the input to one or more other work queues, and so on. This forms a series of 
processing steps that respond to events, with the events being the **completion of the preceding step** in the work 
queue that came before it.

These sort of event-driven processing systems are often called **workflow systems**, since there is a flow of work 
through a directed, acyclic graph that describes the various stages and their coordination.

As shown below, this workflow combines copying work into multiple queues (Stage 2a, 2b) parallel processing of those 
queues, and combining the result back into a single queue (Stage 3).

<img width="351" alt="image" src="https://user-images.githubusercontent.com/47337188/243149584-c8c4c3b1-ffef-4019-a51b-3fa7df76b0d1.png">

### Patterns of Event-Driven Processing

The simplest pattern—one where the output of a single queue becomes the input to a second queue—is straightforward enough that we won’t cover it here.

We will describe patterns that involve the **coordination** of multiple different queues or the **modification** of the output of one or more work queues.

**Copier**

The job of a copier is to take a single stream of work items and duplicate it out into two or more identical streams. 

**Filter**

The role of a filter is to reduce a stream of work items to a smaller stream of work items by filtering out work items that don’t meet particular criteria. 

**Splitter**

The role of a splitter is to evaluate some criteria—just like a filter—but instead of eliminating input, the splitter sends different inputs to different queues based on that criteria.

**Sharder**

A slightly more generic form of splitter is a sharder. Much like the sharded server that we saw in earlier chapters, 
the role of a sharder in a workflow is to divide up a single queue into an evenly divided collection of work items 
based upon some sort of sharding function. There are several different reasons why you might consider sharding your 
workflow. One of the first is for **reliability**. An additional reason to shard your work queue is to more **evenly** 
**distribute** work across different resources.

**Merger**

A merger is the opposite of a copier; the job of a merger is to take two different work queues and turn them into a single work queue.

### Publisher/Subscriber Infrastructure

We need to figure out how to manage the stream of data that passes through the event-driven workflow. The simplest 
thing to do would be to simply write each element in the work queue to a particular directory on a **local filesystem**, 
and then have each stage monitor that directory for input.

But of course doing this with a local filesystem limits our workflow to operating on a single node. We can introduce 
a **network filesystem** to distribute files to multiple nodes, but this introduces increasing complexity both in our 
code and in the deployment of the batch workflow.

Instead, a popular approach to building a workflow like this is to use a publisher/subscriber (pub/sub) API or 
service. A pub/sub API allows a user to define a collection of queues (sometimes called topics). One or more 
publishers publishes messages to these queues. Likewise, one or more subscribers is listening to these queues for 
new messages. When a message is published, it is reliably stored by the queue and subsequently delivered to 
subscribers in a reliable manner.

## Coordinated Batch Processing

Duplicating and producing multiple different outputs is often an important part of batch processing, but sometimes 
it is equally important to pull multiple outputs back together in order to generate some sort of aggregate output.

Probably the most canonical example of this aggregation is the reduce part of the MapReduce pattern. It’s easy to 
see that the map step is an example of sharding a work queue, and the reduce step is an example of coordinated 
processing that eventually reduces a large number of outputs down to a single aggregate response.

Below are some coordinated batch processing patterns.

### Join (or Barrier Synchronization)

Join is similar to joining a thread. The basic idea is that all of the work is happening in parallel, but work items 
aren’t released out of the join until all of the work items that are processed in parallel are completed. This is 
also generally known as barrier synchronization in concurrent programming.

The value of the join is that it ensures that all of the data in the set is present. The downside of the join 
pattern is that it requires that all data be processed by a previous stage before subsequent computation can begin. 
This reduces the parallelism that is possible in the batch workflow, and thus increases the overall latency of 
running the workflow.

### Reduce

With the reduce pattern, each step in the reduce merges several different outputs into a single output. This stage 
is called “reduce” because it reduces the total number of outputs. Additionally, it reduces the data from a complete 
data item to simply the representative data necessary for producing the answer to a specific batch computation.

Because the reduce phase operates on a range of input, and produces a similar output, the reduce phase can be 
repeated as many or as few times as necessary in order to successfully reduce the output down to a single output for 
the entire data set. This is a fortunate contrast to the join pattern, because unlike join, it means that reduce can 
be started in parallel while there is still processing going on as part of the map/shard phase. Of course, in order 
to produce a complete output, all of the data must be processed eventually, but the ability to begin early means 
that the batch computation executes more quickly overall.

## Conclusion (of the book)

Throughout the history of software development and technology, new abstraction layers and patterns have emerged to 
simplify and accelerate the software building process. The introduction of compilers and programming languages paved 
the way, followed by object-oriented programming languages and managed code. Each of these advancements encapsulated 
expert knowledge and practices into algorithms and patterns that could be adopted by a wider range of developers.

Patterns like sidecars, ambassadors, sharded services, FaaS, work queues, and more can form the foundation on which 
modern distributed systems are built. Distributed system developers should no longer be building their systems from 
scratch as individuals but rather collaborating together on reusable, shared implementations of canonical patterns 
that form the basis of all of the systems we collectively deploy.

# References

Designing Distributed Systems By Brendan Burns
