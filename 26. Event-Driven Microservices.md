# Event-Driven Microservices

## Intro
While there are numerous benefits to microservices architecture, like easier deployment and testing, improved productivity, flexibility, and scalability, they also pose a few disadvantages, as independently run microservices require a seamless method of communication to operate as one larger application.

Event-driven microservices allow for real-time microservices communication, enabling data to be consumed in the form of events before they’re even requested.

An event is a change in state, or an update. Events can either carry the state (the item purchased, its price, and a delivery address) or events can be identifiers (a notification that an order was shipped).

Traditional messaging middleware is not only non-distributed and therefore not scalable, but it also
lacks persistent storage as a core characteristic. With a traditional messaging server, messages are
persisted in queues until the server attempts a delivery, which is not guaranteed. This poses challenges
when we need to add a new service and want it to consume historical events.

An event-driven microservice must be able to replay historical events and messages that occurred prior to the existence of the service.

Apache Kafka, Amazon Kinesis, Rabbit MQ are examples of a distributed data streaming platform that are a popular event processing choice. They can handle publishing, subscribing to, storing, and processing event streams in real time. 

## Event-driven architecture

Event-driven architectures have 3 key components: event producers, event routers, and event consumers. A producer publishes an event to the router, which filters and pushes the events to consumers. Producer services and consumer services are decoupled, which allows them to be scaled, updated, and deployed independently.

Here's an example of an event-driven architecture for an e-commerce site.

![image](https://user-images.githubusercontent.com/47337188/175828059-329fbf59-d630-4719-b33f-9b0e1c2a2429.png)

It’s important to realize that like any microservice implementation, an event-driven architecture is a distributed system. Which means the system’s components are located on different networked computers, which communicate and coordinate their actions over the network in order to achieve a common goal.

### Challenges

- Reason about the system

  In REST microservices you can see the direct interactions between microservices from the code. In an event-driven architecture, looking at the code of a producer gives no evidence of what happens once an event is produced.
- Reason about data

  With the database-per-service model it becomes more difficult, especially if data is replicated to other microservices.
- Design events

  Since any consumer can subscribe to the event, it has to be re-usable instead of being tailored to the exact needs of one consumer. At the same time, it cannot be generic to the point where the intent becomes unclear.
- Design for failures

  Assuming at-least-once delivery guarantees are used (by far the most common), the broker will send the event to the consumer again. If events are not designed to deal with these realities, it will cause widespread data consistency issues.
- Design and track event flows

  While components in the system are loosely coupled, and fairly autonomous as a result, in the end the system overall needs to perform business transactions.
- Changing events

  Systems change over time, meaning that events change as well in order to facilitate the new behaviors of the system. Changing events without impacting other microservices can prove difficult, especially in a scaled setting when teams are not on top of keeping track of who consumes the events they produce. When events are persisted and replayed, the system also needs to be able to parse all historic versions of an event, which can cause massive complexity over time.
- Synchronous flows

  Due to the asynchronous nature of events facilitating synchronous behaviors is not where this architecture shines. The recommendation is facilitating these operations with REST, which is a much better pattern for synchronous request-reply.
  



## *References
https://aws.amazon.com/event-driven-architecture/

https://medium.com/swlh/the-engineers-guide-to-event-driven-architectures-benefits-and-challenges-3e96ded8568b

https://www.confluent.io/resources/event-driven-microservices/?utm_medium=sem&utm_source=google&utm_campaign=ch.sem_br.nonbrand_tp.prs_tgt.technical-research_mt.mbm_rgn.namer_lng.eng_dv.all_con.event-driven-microservices&utm_term=%2Bevent%20%2Bdriven%20%2Bmicroservices&creative=&device=c&placement=&gclid=CjwKCAjw46CVBhB1EiwAgy6M4kalZAbypNmN_8ySiBAj8v3l0YKZfqx1qk4mulkqEGDKYvu3UBduyRoCLV8QAvD_BwE
