# Serving Patterns

In contrast to single-node patterns, the multi-node distributed patterns are more **loosely coupled**. While the 
patterns dictate patterns of communication between the components, this communication is based on **network calls**. 
Furthermore, many calls are issued in parallel, and systems coordinate via loose **synchronization** rather than tight 
constraints.

## Replicated Load-Balanced Services

<img width="644" alt="image" src="https://user-images.githubusercontent.com/47337188/243011256-2e97cbe4-b016-4f1f-8f5d-6ecb030d512b.png">

In such a service, every server is identical to every other server and all are capable of supporting traffic. The 
pattern consists of a scalable number of servers with a load balancer in front of them.

Many applications require some time to become **initialized** before they are **ready** to serve. They may need to connect 
to databases, load plugins, or download serving files from the network. In all of these cases, the containers are 
alive, but they are not ready. It is important to build and deploy a **readiness probe** to inform the **load balancer**.

Often there are reasons for wanting to ensure that a particular user’s requests always end up on the same machine. 
**Session tracking** is performed by hashing the source and destination IP addresses and using that key to identify the 
server that should service the requests.

Sometimes the code in your stateless service is still expensive despite being stateless. In such a world, a **caching** 
layer can make a great deal of sense. A cache exists between your stateless application and the end-user request. 
The simplest form of caching for web applications is a **caching web proxy**. The caching proxy is simply an HTTP server 
that maintains user requests in memory state. If two users request the same web page, only one request will go to 
your backend; the other will be serviced out of memory in the cache, as shown below.

<img width="634" alt="image" src="https://user-images.githubusercontent.com/47337188/241821607-d944d455-e74d-4c2d-a1e2-93bbca353f01.png">

It also makes sense to add general denial-of-service defense via **rate limiting** to the caching layer.

## Sharded Services

In contrast to replicated services, with sharded services, each replica, or shard, is only capable of serving a 
subset of all requests. A load-balancing node, or **root**, is responsible for examining each request and distributing 
each request to the appropriate shard or shards for processing.

**Replicated** services are generally used for building **stateless** services, whereas **sharded** services are generally used 
for building **stateful** services. The primary reason for sharding the data is because the size of the state is too 
large to be served by a single machine.

A sharded **cache** is a cache that sits between the user requests and the actually frontend implementation.

<img width="411" alt="image" src="https://user-images.githubusercontent.com/47337188/241822847-c57cc18e-dfd6-4c29-aa1e-897eeace973f.png">

Sometimes your system is so dependent on a cache for latency or load that it is not acceptable to lose an entire 
cache shard if there is a failure or you are doing a rollout. Alternatively, you may have so much load on a 
particular cache shard that you need to **scale** it to handle the load. For these reasons, you may choose to deploy 
a **sharded**, **replicated** service. A sharded, replicated service combines the replicated service pattern with 
the sharded pattern.

A **sharding function** is very similar to a **hashing function**: `Shard = ShardingFunction(Req)`. For our sharded service, 
**determinism** and **uniformity** are the most important characteristics. Determinism is important because it ensures that 
a particular request R always goes to the same shard in the service. Uniformity is important because it ensures that 
load is evenly spread between the different shards.

## Scatter/Gather

So far we’ve examined systems that replicate for scalability in terms of the number of **requests** processed per second 
(the stateless replicated pattern), as well as scalability for the size of the **data** (the sharded data pattern). In 
this chapter we introduce the scatter/gather pattern, which uses replication for scalability in terms of **time**. 
Specifically, the scatter/gather pattern allows you to achieve parallelism in servicing requests, enabling you to 
service them significantly faster than you could if you had to service them sequentially.

Like replicated and sharded systems, the scatter/gather pattern is a tree pattern with a **root** that distributes 
requests and leaves that process those requests. However, in contrast to replicated and sharded systems, with 
scatter/gather requests are **simultaneously** farmed out to all of the replicas in the system. Each replica does a 
small amount of processing and then returns a fraction of the result to the root. The root server then **combines** the 
various partial results together to form a single complete response to the request and then sends this request back 
out to the client.

<img width="508" alt="image" src="https://user-images.githubusercontent.com/47337188/242439085-5ab1f4bd-d5de-4ad6-a0ca-5dbb0fb07b1d.png">

## Functions and Event-Driven Processing

There is a class of applications that might only need to temporarily come into existence to handle a single request, 
or simply need to respond to a specific event. This style of request or event-driven application design has 
flourished recently as large-scale public cloud providers have developed **function-as-a-service** (FaaS) products.

In many cases, FaaS is a component in a broader architecture rather than a complete solution.

### The Benefits of FaaS

The benefits of FaaS are primarily for the developer. It dramatically simplifies the distance from code to running 
service. Because there is no artifact to create or push beyond the source code itself, FaaS makes it simple to go 
from **code on a laptop or web browser** to running **code in the cloud**.

Likewise, the code that is deployed is managed and scaled automatically. As more traffic is loaded onto the service, 
more instances of the function are created to handle that increase in traffic. If a function fails due to 
application or machine failures, it is automatically restarted on some other machine.

Finally, much like containers, functions are an even more granular building block for designing distributed systems. 
Functions are stateless and thus any system you build on top of functions is inherently more modular and decoupled 
than a similar system built into a single binary.

### The Challenges of FaaS

Each function is entirely independent. The only communication is across the network, and each function instance 
cannot have local memory, requiring all states to be stored in a storage service. This forced decoupling can improve 
the agility and speed with which you can develop services, but it can also significantly complicate the operations 
of the same service.

### Patterns for FaaS

**The Decorator Pattern: Request or Response Transformation**

FaaS is ideal for deploying simple functions that can take an input, transform it into an output, and then pass it 
on to a different service. This general pattern can be used to augment or decorate HTTP requests to or from a 
different service.

**Handling Events**

Because these events tend to be largely independent and stateless in nature, and because the rate of events can be 
highly variable, they are ideal candidates for event-driven and FaaS architectures.

A concrete example of integrating an event-based component to an existing service is implementing two-factor 
authentication. In this case, the event is the user logging into a service. The service can generate an event for 
this action, fire it into a function-based handler that takes the code and the user’s contact information, and sends 
the two-factor code via text message.

**Event-Based Pipelines**

In the event pipeline pattern, each node is a different function or webhook, and the edges linking the graph 
together are HTTP or other network calls to the function/webhook. In general, there is no shared state between the 
different pieces of the pipeline, but there may be a context or other reference point that can be used to look up 
information in shared storage.

# References

Designing Distributed Systems By Brendan Burns

