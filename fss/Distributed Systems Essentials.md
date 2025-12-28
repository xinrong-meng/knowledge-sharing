# Distributed Systems Essentials

## Communications Basics

### Communications Hardware

Different types of communications **channels** exist. The most obvious categorization is **wired** versus 
**wireless**. For each category there are multiple network transmission hardware technologies that can ship bits 
from one machine to another. Each technology has different characteristics, and the ones we typically care about are 
**speed** and **range**.

From a distributed systems software perspective, we need to understand more about the **“magic”** that enables all this 
hardware to route messages from, say, my cell phone to my bank and back. This is where the Internet Protocol (IP) 
comes in.

### Communications Software

Software systems on the internet communicate using the Internet Protocol (IP) suite. The IP suite specifies host 
addressing, data transmission formats, message routing, and delivery characteristics. There are four abstract layers,
which contain related protocols that support the functionality required at that layer. These are, from lowest to 
highest:

- The **data link** layer, specifying communication methods for data across a single network segment. This is 
implemented by the device drivers and network cards that live inside your devices.
- The **internet** layer specifies addressing and routing protocols that make it possible for traffic to traverse the 
independently managed and controlled networks that comprise the internet. This is the IP layer in the internet protocol suite.
- The **transport** layer, specifying protocols for reliable and best-effort, host-to-host communications. This is 
where the well-known Transmission Control Protocol (TCP) and User Datagram Protocol (UDP) live.
- The **application** layer, which comprises several application-level protocols such as HTTP and the secure copy 
protocol (SCP).

Each of the higher-layer protocols builds on the features of the lower layers. 

## Remote Method Invocation

It’s perfectly feasible to write our distributed applications using low-level APIs that interact directly with the 
**transport layer** protocols TCP and UDP. The most common approach is the standardized **sockets** library.

This is something you’ll hopefully never need to do, as sockets are complex and error prone. There are (luckily) 
much better ways to build distributed communications, as I’ll describe in this section. These approaches abstract 
away much of the complexity of using sockets. However, sockets still lurk underneath, so some knowledge is necessary.

### Sockets

A socket is one **endpoint** of a two-way network connection between a client and a server. Sockets are identified by a 
combination of the node’s **IP address** and an abstraction known as a **port**. A port is a unique numeric identifier, 
which allows a node to support communications for multiple applications running on the node.

Each IP address can support 65,535 TCP ports and another 65,535 UDP ports. On a server, each `{<IP Address>, <port>}`
combination can be associated with an application. 

A socket connection is identified by a unique combination of client and server IP addresses and ports, namely 
<client IP address, client port, server IP address, server port>.

Socket APIs are available in all mainstream programming languages. 

### Object-oriented

Stepping back, if we were defining a mobile banking server interface in an object-oriented language such as Java, we 
would have each operation it can process as a method. Each method is passed an appropriate parameter list for that 
operation, as shown in this example code:

```java
public interface IGBank {
    public float balance  (String accNo);
    public boolean statement(String month) ;
    // other operations
}
```

There are several advantages of having such an interface, namely:

- **Calls from the client** to the server can be statically checked by the compiler to ensure they are of the correct 
format and argument types.
- **Changes in the server interface** (e.g., adding a new parameter) force changes in the client code to adhere to the 
new method signature.
- **The interface is clearly defined** by the class definition and thus straightforward for a client programmer to 
understand and utilize.

### RPC/RMI

These benefits of an **explicit interface** are of course well known in software engineering. The whole discipline of 
object-oriented design is pretty much based upon these foundations, where an interface defines a contract between 
the caller and callee. Compared to the implicit application protocol we need to follow with sockets, the advantages 
are significant.

This fact was recognized reasonably early in the creation of distributed systems. Since the early 1990s, we have 
seen an evolution of technologies that enable us to define explicit server interfaces and call these across the 
network using essentially the same syntax as we would in a sequential program. Collectively, they are known as 
Remote Procedure Call (RPC), or Remote Method Invocation (RMI) technologies.

Regardless of the precise implementation, the basic attraction of RPC/RMI approaches is to provide an abstract 
calling mechanism that supports location transparency for clients making remote server calls. Location transparency 
is provided by the registry, or in general any mechanism that enables a client to locate a server through a 
directory service. This means it is possible for the server to update its network location in the directory without 
affecting the client implementation.

RPC/RMI is not without its flaws. Marshalling and unmarshalling can become inefficient for complex object parameters.
Cross-language marshalling—client in one language, server in another—can cause problems due to types being 
represented differently in different languages, causing subtle incompatibilities. And if a remote method signature 
changes, all clients need to obtain a new compatible stub, which can be cumbersome in large deployments.

For these reasons, most modern systems are built around simpler protocols based on HTTP and using JSON for parameter 
representation. Instead of operation names, HTTP verbs (PUT, GET, POST, etc.) have associated semantics that are 
mapped to a specific URL.

## Consensus in Distributed Systems

In reality, distributed systems reach consensus all the time. This is possible because while our networks are 
asynchronous, we can establish sensible practical bounds on message delays and retry after a timeout period.

## Time in Distributed Systems

Every node in a distributed system has its own internal clock. If all the clocks on every machine were perfectly 
synchronized, we could always simply compare the timestamps on events across nodes to determine the precise order 
they occurred in.

Unfortunately, this is not the case. Clocks on individual nodes drift due to environmental conditions like changes 
in temperature or voltage. The amount of drift varies on every machine, but values such as 10–20 seconds per day are 
not uncommon.

If left unchecked, clock drift would render the time on a node meaningless. To address this problem, a number of 
time services exist. A **time service** represents an accurate time source, such as a GPS or atomic clock, which can be 
used to periodically reset the clock on a node.

The most widely used time service is Network Time Protocol (NTP), which provides a hierarchically organized 
collection of time servers spanning the globe. Using the NTP protocol, a node in an application running an NTP 
client can synchronize to an NTP server. The time on a node is set by a UDP message exchange with one or more NTP 
servers. Messages are time stamped, and through the message exchange the time taken for message transit is estimated.
This becomes a factor in the algorithm used by NTP to establish what the time on the client should be reset to.

In fact, a compute node has two clocks. These are:

- Time of day clock: 
This represents the number of milliseconds since midnight, January 1st 1970. In Java, you can get the current time 
using System.currentTimeMillis(). This is the clock that **can be reset by NTP**, and hence may jump forward or backward 
if it is a long way behind or ahead of NTP time.

- Monotonic clock: This represents the amount of time (in seconds and nanoseconds) since an unspecified point in the 
  past, such as the 
last time the system was restarted. It will only ever move forward; however, it again may not be a totally accurate 
measure of elapsed time because it stalls during an event such as virtual machine suspension. In Java, you can get 
the current monotonic clock time using Sys⁠tem.nanoTime().

The takeaway from this discussion is that our applications cannot rely on timestamps of events on different nodes to 
represent the actual order of these events.

## References

Foundations of Scalable Systems By Ian Gorton
