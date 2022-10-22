# API Gateway

## What & Why

An API gateway sits between clients and services. It acts as a reverse proxy, routing requests from clients to services.

It may also perform various tasks such as authentication, SSL termination*, and rate limiting.

If you don't deploy a gateway, clients must send requests directly to front-end services.

However, there are some potential problems with exposing services directly to clients:

- It can result in complex client code. The client must keep track of multiple endpoints, and handle failures in a 
resilient way.
- It creates coupling between the client and the backend. The client needs to know how the individual services are 
  decomposed. That makes it harder to maintain the client and also harder to refactor services.
- A single operation might require calls to multiple services. That can result in multiple network round trips 
  between the client and the server, adding significant latency.
- Each public-facing service must handle concerns such as authentication, SSL, and client rate limiting.
- Services must expose a client-friendly protocol such as HTTP or WebSocket. This limits the choice of communication 
  protocols.
- Services with public endpoints are a potential attack surface, and must be hardened.

A gateway helps to address these issues by decoupling clients from services. Gateways can perform a number of 
different functions. The functions can be grouped into the following design patterns:

- **Gateway Routing**. Use the gateway as a reverse proxy to route requests to one or more backend services, using 
  layer 7 routing. The gateway provides a single endpoint for clients, and helps to decouple clients from services.
- **Gateway Aggregation**. Use the gateway to aggregate multiple individual requests into a single request. This pattern 
applies when a single operation requires calls to multiple backend services. The client sends one request to the gateway. The gateway dispatches requests to the various backend services, and then aggregates the results and sends them back to the client. This helps to reduce chattiness between the client and the backend.
- **Gateway Offloading**. Use the gateway to offload functionality from individual services to the gateway, particularly 
cross-cutting concerns. It can be useful to consolidate these functions into one place, rather than making every service
responsible for implementing them. This is particularly true for features that requires specialized skills to 
  implement correctly, such as authentication and authorization.

Here are some examples of functionality that could be offloaded to a gateway:

- SSL termination
- Authentication
- IP allow/block list
- Client rate limiting (throttling)
- Logging and monitoring
- Response caching
- Web application firewall
- GZIP compression
- Servicing static content

## Caveats of using API Gateways

First, an API Gateway is a new software component that a DevOps (or APIOps) team needs to deploy, configure, and 
maintain. This means there’s an extra moving part in the architecture, which means additional cost (money, time, effort) and a learning curve.

Adding an extra component between clients and the microservices means an extra network hop for requests. Depending 
on the network speed, this can have an adverse effect on the service response time.

As the entry point for all your services, an API Gateway could potentially become a single point of failure and take 
your entire system offline when it becomes unavailable. For this reason, API gateways are often configured to be highly availability (HA).

Similarly, an API Gateway can be a single point of attack for hackers and malicious players. A compromised API 
Gateway can expose your microservices to further attacks.

## <> Load balancer

From the perspective of the API gateway, the requests themselves are being balanced. It’s more important to take the 
request and ensure that they are properly formatted, hitting the correct microservice, and are being equalized to 
prioritize resource service. However, API gateways can do so much more than simple routing. They often offer 
authentication, compliance, and other verification systems to ensure that the request has the best chance of being 
served.

Load balancers, on the other hand, are less concerned with the requests and are much more concerned with the network 
traffic. In other words, Load balancers balance the network, not the requests. A load balancer doesn’t really care 
whether the request is well-formed or which microservices the server is sending to — instead, it cares whether the 
resource that can solve the request is free to do so and whether it is overly taxed with network demands.

## *References

https://www.redhat.com/en/topics/api/what-does-an-api-gateway-do

https://microservices.io/patterns/apigateway.html

https://konghq.com/learning-center/api-gateway/why-microservices-need-api-gateway

https://nordicapis.com/whats-the-difference-between-an-api-gateway-and-a-load-balancer/

### Terms
**SSL termination**: The process of decrypting encrypted traffic before passing it along to a web server
