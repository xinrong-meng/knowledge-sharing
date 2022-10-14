# Service-Oriented Architecture

## History
SOA dates to 2009, when the Open Group described it in a white paper that eventually became the SOA Source Book. The 
Open Group defines SOA as “an architectural style that supports service-orientation. Service-orientation is a way of 
thinking in terms of services and service-based development and the outcomes of services.”

The initial aim of SOA was to make the IT landscape more flexible and provide real-time communication between 
applications. Prior to SOA, most enterprise application communication took place via direct client-server calls, 
such as remote procedure calls (RPC).

Drawbacks of direct application-to-application communication:
- **Coupling** with the underlying application runtime environment.
  Applications that want to communicate, for example, via RPC methods, require the same client-server libraries and 
  protocols. This doesn’t allow for great application diversity because not all libraries and protocols may be 
  available for all languages. 
- **Compatibility**; versioning is more difficult to manage. If an application method changes, the 
  other application also needs to change immediately, otherwise it might break. 
- **Scalability**: once the number of applications increases, the number of interfaces quickly 
  becomes unmanageable.

These drawbacks are the main reasons why SOA model exists.

## Definition
Communication between applications through web services. It is about exposing business functionality. Some people 
call these services, others APIs.

SOA is also used for abstracting and hiding application complexity because within SOA the applications (and their 
complexity) disappear into the background. Business functionality is provided instead.

SOA standardized the way applications communicate. Within SOA, application communication is done via standardized 
protocols, such as SOAP or JSON, and common software architectural styles, such as REST*. SOA is about synchronous 
communication (waiting for the reply in order to continue) and asynchronous communication (not waiting).

### REST

REST is an architectural style that defines a set of constraints and abstraction principles to be used for creating web
services. A key concept in REST is resources. Resources can be any object or source of information that can be 
uniquely identified, such as a customer, contract, account, order, or product. For RESTful APIs, the HTTP protocol 
has set operations for interacting with these resources:

**POST**

A create method for creating a new resource.

**GET**

A read method for retrieving one or multiple (full list) resources.

**PUT**

A method to update or replace any existing resource. For updating only specific fields within a resource, PATCH is 
more commonly used.

**DELETE**

A method to delete a specific resource.

These primitive operations are often combined with the CRUD (create, read, update, delete) method. Where REST is the 
API protocol style, CRUD is the interaction style for manipulating data.

## Enterprise Service Bus

The enterprise service bus (ESB), part of SOA, handle communication between different applications.

Instead of communicating directly to each other, applications communicate via the ESB.

![image](https://user-images.githubusercontent.com/47337188/195851263-78f19b01-04bc-4ff8-9a2c-573efa667dfc.png)

The ESB decouples systems from each other, allowing them to communicate without dependency on or knowledge of other 
systems on the bus. The concept of ESB was born out of the need to move away from point-to-point integration, which 
becomes brittle and hard to manage over time. Point-to-point integration results in custom integration code being 
spread among applications with no central way to monitor or troubleshoot. This is often referred to as "spaghetti 
code" and does not scale because it creates tight dependencies between applications.

### Implementation

- The "bus" concept decouples applications from each other. This is usually achieved using a messaging server like 
JMS or AMQP.
- The data that travels on the bus is a canonical format and is almost always XML.
- There is an "adapter" between the application and the bus that marshals data between the two parties.
- The adapter is responsible for talking to the backend application and transforming data from the application format 
  to the bus format. The adapter can also perform a host of other activities such as message routing transaction 
  management, security, monitoring, error handling, etc.
- ESBs are generally stateless; the state is embedded in the messages passing through the bus.
- The canonical message format is the contract between systems. The canonical format means that there is one 
  consistent message format traveling on the bus and that every application on the bus can communicate with each other.



## < > Microservices

The main distinction between the two approaches comes down to **scope**. To put it simply, SOA has an enterprise scope, 
while the microservices architecture has an application scope.

![image](https://user-images.githubusercontent.com/47337188/195856658-a8a01e94-2a83-45b1-a1c4-4d26fd03d5fd.png)


Both SOA and microservices can use automation to speed up business processes. Larger, more diverse environments tend 
to lean towards service-oriented architecture (SOA), which supports integration between heterogenous applications 
and messaging protocols via an enterprise-service bus (ESB). Smaller environments, including web and mobile 
applications, do not require such a robust communication layer and are easier to develop using a microservices 
architecture.

## *References
https://martinfowler.com/bliki/ServiceOrientedAmbiguity.html

Data Management at Scale - By Piethein Strengholt

https://www.ibm.com/cloud/blog/soa-vs-microservices

https://www.mulesoft.com/resources/esb/what-esb




