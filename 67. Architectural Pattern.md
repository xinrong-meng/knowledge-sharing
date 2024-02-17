# Architectural Patterns

## What are Architectural Patterns

Architectural patterns are reusable solutions to common problems encountered in software architecture and design. 
These patterns provide a structured way to design and organize the components of a software system to achieve 
specific goals such as scalability, maintainability, and flexibility.

### vs. Design Patterns

| Aspect               | Design Patterns | Architectural Patterns |
|----------------------|-----------------|------------------------|
| **Scope**                | Class-level solutions | Overall structure of systems |
| **Purpose**              | Address specific design issues | Organize entire systems |
| **Granularity**          | Deal with classes or objects | Modules, components, relationships |
| **Level of Abstraction** | Low-level implementation | High-level system structure |
| **Examples**             | Singleton, Factory Method, etc. | MVC, Microservices, etc. |
| **Usage**                | Within a single application | For entire systems |
| **Common Goals**         | Reusability, maintainability | Scalability, flexibility |

## Common Architectural Patterns

### 1. Client-Server

**Description**

Segregates the system into two applications, where the client makes requests to the server which then
processes and returns the data.

**Use Case**

Web applications where the browser acts as the client and an application on a server handles the backend.

### 2. Peer-to-Peer (P2P)

**Description**

Each node in the network acts as both a server and a client, eliminating the need for a centralized server.

**Use Case**

File-sharing systems like BitTorrent, blockchain applications.

**vs. Client-Server**

| Feature | Client-Server Architecture | Peer-to-Peer (P2P) Architecture |
|---------|----------------------------|--------------------------------|
| **Basic Concept** | Centralized server provides resources or services; clients consume these services. | Decentralized network where each peer acts as both client and server. |
| **Network Structure** | Centralized with one or more servers at the core. | Decentralized with no central server; all nodes are equal. |
| **Scalability** | Can be limited by the capacity of the server(s); requires scaling the server resources as demand increases. | Naturally scalable as each new peer adds to the network's capacity. |
| **Resource Distribution** | Server holds the resources, and clients request them. | Resources are distributed among peers; each peer can provide and consume resources. |
| **Fault Tolerance** | Single point of failure at the server; if the server goes down, the service is interrupted. | Highly resilient; if one peer fails, others can still operate and communicate. |
| **Control and Management** | Centrally managed by server administrators. | Lacks central management, which can lead to challenges in control and regulation. |
| **Use Cases** | Web servers, database servers, email servers, etc. | File sharing networks, blockchain and cryptocurrencies, certain streaming services. |
| **Security** | Security can be more straightforward to implement and manage due to centralized control. | Potentially more vulnerable to security risks due to its open and decentralized nature. |

### 3. Layered (N-Tier)

**Description**

Separates system functionality into distinct layers that are stacked vertically on top of each other. 
Common layers include presentation, business logic, data access, and data storage.

**Use Case**

How a web application is internally structured on the server side. The application is divided into layers 
such as a front-end (for user interface), a business logic layer (where the main functionality of the application 
resides), and a data layer (for database interactions). Each layer has a specific responsibility and they 
communicate with each other in a defined order.

### 4. Model-View-Controller (MVC)

**Description**

Model: Manages data and business logic.

View: Handles the display and presentation of data.

Controller: Connects the Model and View, processing user input and responding to user actions.

**Use Case**

Web frameworks like Django and Ruby on Rails, desktop applications.

**vs. Layered**

| Aspect | MVC | Layered |
|--------|-----|----------------------|
| Focus | User interface interactions | Organizational code structure |
| Components | Model, View, Controller | Presentation, Business Logic, Data Access Layers |
| Data Flow | Cyclical (View <-> Controller <-> Model) | Linear (Top to Bottom) |
| Use Cases | Web and GUI applications | Web, Desktop, Enterprise applications |

### 5. Microservices

**Description**

Structures an application as a collection of loosely coupled services, which implement business 
capabilities.

**Use Case**

Large-scale enterprise applications that require high scalability and flexibility.

### 6. Service-Oriented Architecture (SOA)

**Description**

Consists of services that communicate with each other. The communication can involve either simple data passing or 
it could involve two or more services coordinating some activity.

**Use Case**

Enterprise applications requiring integration of multiple disparate systems.

**vs. Microservices**

| Feature | Service-Oriented | Microservices |
|---------|-------------------------------------|---------------|
| **Scope** | Enterprise-wide services, often larger and more generalized. | Smaller, lightweight services focused on specific business capabilities. |
| **Communication** | Often uses Enterprise Service Bus (ESB) for communication, which can become complex. | Uses simpler, decentralized communication mechanisms like RESTful APIs. |
| **Service Size** | Services are generally larger and can encompass broad business functionalities. | Services are smaller, highly specialized based on single business capability. |
| **Technology Stack** | Typically follows a standardized, often homogeneous technology stack. | Encourages the use of different technology stacks suitable for each service. |
| **Integration and Coupling** | Services are more tightly coupled and can share data storage. | Services are loosely coupled, each with its own data storage, ensuring high autonomy. |
| **Development and Deployment** | Development and deployment can be slower due to larger service size and shared dependencies. | Enables rapid, independent development and deployment of individual services. |
| **Management and Scalability** | Centralized management, which can be complex in large enterprises. | Easier to scale and manage due to smaller, independent services. |
| **Use Cases** | Suitable for large-scale enterprise applications requiring integration of various applications and systems. | Ideal for complex applications with requirements for rapid development, scalability, and resilience. |

### 7. Monolithic

**Description**

Builds the entire application as a single, indivisible unit.

**Use Case**

Simple applications with limited scalability and flexibility requirements.

### 8. Event-Driven

**Description**

Centers around the production, detection, consumption of, and reaction to events.

**Use Case**

Real-time data processing applications, applications with asynchronous data flow.

## Combining Architectural Patterns

Combining architectural patterns is a common practice in software design, allowing architects to leverage the 
strengths of multiple patterns to address complex requirements. Here are a few examples of how different 
architectural patterns can be combined.

### Microservices and Event-Driven

In a microservices architecture, services can communicate with each other using events rather than direct calls. 
This decouples the services and reducing dependencies.

Event-driven architecture also enables microservices to react to changes in real-time. When an event occurs (like a 
data update), relevant microservices can immediately respond, making the system more dynamic and responsive.

By using events, microservices can handle requests asynchronously, improving system performance and scalability.

### Layered and Service-Oriented

Layered Architecture can organize the internal structure of each SOA service, making it easier to manage and maintain.

### Client-Server and Model-View-Controller

Client-Server Architecture acts as the fundamental structure for network communication, where the client could be a 
web browser or mobile app, and the server is the application server hosting the business logic and data access 
layers.

Model-View-Controller Architecture organizes the server-side application structure. The server, in this combined 
architecture, likely implements the MVC pattern to manage data (Model), handle business logic (Controller), and 
serve the user interface (View).

## References

ChatGPT 4