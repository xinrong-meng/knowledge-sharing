# Distributed Systems Architectures: An Introduction

## Basic System Architecture

A typical very simple software architecture for “starter” systems, which closely resembles what you get with rapid
development frameworks, is shown as below.

![image](https://user-images.githubusercontent.com/47337188/253133123-62b4d70e-c44c-4a38-9885-ce500433008d.png)

This comprises a client tier, application service tier, and a database tier. If you use Rails or equivalent, you 
also get a framework which hardwires a model–view–controller (MVC) pattern for web application processing and an 
object–relational mapper (ORM) that generates SQL queries.

This approach leads to what is generally known as a monolithic architecture. Monoliths tend to grow in complexity 
as the application becomes more feature-rich. All API handlers are built into the same server code body. This 
eventually makes it hard to modify and test rapidly, and the execution footprint can become extremely heavyweight as 
all the API implementations run in the same application service.

In this case, the first strategy for scaling is usually to “scale up” the application service hardware. For example, 
if your application is running on AWS, you might upgrade your server from a modest t3.xlarge to a t3.2xlarge 
instance, which doubles the number of CPUs and memory available for the application.

It’s inevitable, however, that for many applications the load will grow to a level which will swamp a single server 
node, no matter how many CPUs and how much memory you have. That’s when you need a new strategy—namely, scaling out, 
or horizontal scaling.

## Scale Out

![image](https://user-images.githubusercontent.com/47337188/253136825-d68fcc93-1822-4ef8-81da-378831756584.png)


To successfully scale out an application, you need two fundamental elements in your design.

- A load balancer

All user requests are sent to a load balancer, which chooses a service replica target to process the request.

- Stateless services

For load balancing to be effective and share requests evenly, the load balancer must be free to send consecutive 
requests from the same client to different service instances for processing. This means the API implementations in 
the services must retain no knowledge, or state, associated with an individual client’s session. When a user 
accesses an application, a user session is created by the service and a unique session is managed internally to 
identify the sequence of user interactions and track session state. A classic example of session state is a **shopping** 
**cart**. To use a load balancer effectively, the data representing the current contents of a user’s cart must be stored 
somewhere—typically a data store—such that any service replica can access this state when it receives a request as 
part of a user session.

At some stage, however, reality will bite and the capability of your single database to provide low-latency query 
responses will diminish. Your database becomes a bottleneck that you must engineer away in order to scale your 
application further.

## Scaling the Database with Caching

Scaling up is a common database scalability strategy.

In conjunction with scaling up, a highly effective approach is querying the database as infrequently as possible 
from your services. This can be achieved by employing distributed caching in the scaled-out service tier. Caching 
stores recently retrieved and commonly accessed database results in memory so they can be quickly retrieved without 
placing a burden on the database.

Still, many systems need to rapidly access terabytes and larger data stores that make a single database effectively 
prohibitive. In these systems, a distributed database is needed.

## Distributing the Database

In very general terms, there are two major categories:

- Distributed SQL stores

These enable organizations to scale out their SQL database relatively seamlessly by storing the data across multiple 
disks that are queried by multiple database engine replicas. These multiple engines logically appear to the 
application as a single database, hence minimizing code changes.

- Distributed so-called “NoSQL” stores (from a whole array of vendors)

These products use a variety of data models and query languages to distribute data across multiple nodes running the 
database engine, each with their own locally attached storage. Again, the location of the data is transparent to the 
application, and typically controlled by the design of the data model using hashing functions on database keys. 

As the data volumes grow, a distributed database can increase the number of storage nodes. As nodes are added (or 
removed), the data managed across all nodes is rebalanced to attempt to ensure the processing and storage capacity 
of each node is equally utilized.

## Multiple Processing Tiers

Any realistic system that you need to scale will have many different services that interact to process a request.

The beauty of the stateless, load-balanced, cached architecture described so far is that it’s possible to extend 
the core design principles and build a multitiered application. In fulfilling a request, a service can call one or 
more dependent services, which in turn are replicated and load-balanced. A simple example is as shown below.

![image](https://user-images.githubusercontent.com/47337188/253144897-4ccb96de-3c90-4daa-8a87-c7cd3526d81b.png)

A major advantage of refactoring monolithic applications into multiple independent services is that they can be 
separately built, tested, deployed, and scaled.

## Increasing Responsiveness

You can decrease response times by using caching and precalculated responses, but many requests will still result in 
database accesses. Some update requests, however, can be successfully responded to without fully persisting the data 
in a database. The data about the event is sent to the service, which acknowledges receipt and concurrently stores 
the data in a remote queue for subsequent writing to the database. Distributed queueing platforms can be used to 
reliably send data from one service to another, typically but not always in a first-in, first-out (FIFO) manner.

Writing a message to a queue is typically much faster than writing to a database, and this enables the request to be 
successfully acknowledged much more quickly. Another service is deployed to read messages from the queue and write 
the data to the database.

These queueing platforms all provide asynchronous communications. A producer service writes to the queue, which acts 
as temporary storage, while another consumer service removes messages from the queue and makes the necessary updates 
to.

The key is that the data **eventually** gets persisted. 

## Systems and Hardware Scalability

Even the most carefully crafted software architecture and code will be limited in terms of scalability if the 
services and data stores run on inadequate hardware.

There are some cases where upgrading the number of CPU cores and available memory is not going to buy you more 
scalability. For example, if code is single threaded. Efficient, multithreaded code is essential to achieving 
scalability.

Adding more hardware always increases costs, but may not always give the performance improvement you expect. 
Running simple experiments and taking measurements is essential for assessing the effects of hardware upgrades.

# References

Foundations of Scalable Systems By Ian Gorton

