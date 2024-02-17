### Microservices Design

## Intro

A microservice is an **independently** **deployable** component of bounded scope that supports **interoperability** through **message-based** communication.

The focus is on building applications that balance **speed** and **safety** at **scale**, primarily through **replaceability**.

From the outside, a single microservice is treated as a **black box**.

It hosts business functionality on one or more **network endpoints**(for example, a queue or a REST API), over whatever protocols are most appropriate. **Consumers**, whether they’re other microservices or other sorts of programs, **access** this functionality via these networked endpoints.

This means microservice architectures **avoid** the use of **shared databases** in most circumstances; instead, each microservice encapsulates its own database where required.

<img width="688" alt="image" src="https://user-images.githubusercontent.com/47337188/168451669-7b12efc7-1f13-4528-98a8-07eeff5db4c8.png">

Microservices embrace the concept of **information hiding**. Information hiding means **hiding as much** information as possible **inside** a component and **exposing as little** as possible via **external** interfaces. This allows for clear **separation** between what can **change easily** and what is more **difficult** to change.


## Design

A microservice **design** **model** comprised of five parts: Service, Solution, Process and Tools, Organization, and Culture.

<img width="777" alt="image" src="https://user-images.githubusercontent.com/47337188/168451677-3afc9063-50b7-46a8-816d-b7b9e899b865.png">

A framework for microservice system designs:

<img width="787" alt="image" src="https://user-images.githubusercontent.com/47337188/168451689-43b97c75-9dcd-4aa9-9591-95922a58fac9.png">


### Case Study: Netflix



* Antifragility

    Netflix works to strengthen their internal systems so that they can withstand unexpected problems.

    Their [Simian Army](https://netflixtechblog.com/the-netflix-simian-army-16e57fbab116) set of tools, which “enforce architectural principles, induce various kinds of failures, and test our ability to survive them”.

* Immutability

    The principle of immutability is used at Netflix to assert that auto-scaled groups of **service** instances are **stateless** and **identical**, which enables Netflix’s system to “scale horizontally.”

* Separation of Concerns(SoC)

    Each team owns a group of services. They **own** building, operating, and evolving those services, and present a stable agreed **interface** and service level agreement to the consumers of those services.



## Service Design


### Microservice Boundaries

So just how micro should a microservice be?

Instead of trying to find some quantity to measure, we find most companies focus on a **quality** of each microservice—the **use case** or **context** in which the component will be used.

There are many ways to **decompose** a large system into smaller subsystems. In one case we may be tempted to decompose a system based on **implementation** **technology**. Alternatively, we can divide a large system based on **team** **geography**.

We may also apply **domain-driven design **to model services around **business domains**.


### API Design for Microservices

Microservice components only become valuable when they can **communicate** with other components in the system. They each have an **interface** or **API**. Just as we need to achieve a high level of separation, independence, and modularity of our **code** we need to make sure that our **APIs**, the component interfaces, are also **loosely coupled**.

Two practices in crafting APIs


#### Message-Oriented

The notion of messaging as a way to share information between components dates back to the initial ideas about how **object-oriented **programming would work.

For example, Netflix relies on message **formats** like Avro, Protobuf, and Thrift over TCP/IP for communicating **internally** and JSON over HTTP for communicating to **external** consumers (e.g., mobile phones, browsers, etc.).


#### Hypermedia-Driven

That takes the notion of message-oriented to the next level.

The messages passed between components contain **more than just data**. The messages also contain **descriptions** of possible **actions**, for example, **links**.

Amazon’s API Gateway support responses in the [Hypertext Application Language (HAL) format](http://stateless.co/hal_specification.html), which defines hypermedia such as **links** to external resources **within** **JSON** or XML code.


## * References

[Microservice Architecture](https://learning.oreilly.com/library/view/microservice-architecture/9781491956328/)

[Building Microservices, 2nd Edition](https://learning.oreilly.com/library/view/building-microservices-2nd/9781492034018/)
