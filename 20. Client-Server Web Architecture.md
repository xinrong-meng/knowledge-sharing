# Client-Server Web Architecture

Here we talk about the Client-Server Architecture in the context of web applications.

The architecture works on a **request-response** model: The client sends the request to the server for information and the server responds with it.

Only a very small percentage of business websites and applications use the **peer-to-peer** architecture, which differs from the client-server.


## Client

The **client** holds our **user interface**. The user interface is the **presentation** part of the application. It’s written in HTML, JavaScript, CSS and is responsible for the **look and feel** of the application.


## Server

The primary task of a web server is to **receive** the requests from the client and provide the **response** after executing the business logic based on the request parameters received from the client.

Servers running web applications are commonly known as application servers. Besides the application servers, there are also other kinds of servers with specific **tasks** assigned. These include: Proxy server, Mail server, File server, Data storage server, etc.


## Communications

**HTTP protocol** is a** request-response** protocol that defines **how** information is transmitted across the web. It’s a **stateless** protocol, and every process over HTTP is executed independently and has no knowledge of previous processes.

In RESTful web applications, every client has to hit a **REST** **endpoint** to fetch the **data** from the backend. This entirely **decouples** the backend and the client code.

<img width="621" alt="image" src="https://user-images.githubusercontent.com/47337188/164861566-0cb836b8-e731-426f-b80e-d31145804ca8.png">

There are two modes of data transfer between the client and the server: HTTP PUSH and HTTP PULL.


### HTTP PULL

The client pulls the data from the server whenever required. It keeps doing this over and over to fetch the latest data.

The client pulls the data in one of two ways:



* send an HTTP GET request to server manually **by human intervention**
* pull data dynamically at regular intervals using **AJAX** without any human intervention

<img width="669" alt="image" src="https://user-images.githubusercontent.com/47337188/164861579-3f230c70-ad3a-4fee-a6f0-b1167a0e64ff.png">


### HTTP PUSH

In this mechanism, the client sends the request for certain information to the server just once. After the first request, the server keeps pushing the new updates to the client whenever they are available.

Below are a few (HTTP) Push-Based technologies.



* Web Sockets

A Web Socket connection is preferred when we need a persistent **bi-directional** low latency data flow from the client to the server and back.

Typical use-cases of web sockets are messaging, chat applications, real-time social streams, browser-based massive multiplayer games, etc. These are apps with quite a **significant number of read writes** compared to a regular web app.

With web sockets, we can keep the client-server connection open as long as we want.

Web sockets don’t work over HTTP. The mechanism runs over **TCP**. Also, the server and the client should both support web sockets. Else it won’t work.



* AJAX  Long polling

Long polling lies somewhere between AJAX and Web Sockets. In this technique, instead of immediately returning the empty response, the server holds the response until it finds an update to be sent to the client.

The connection in long polling stays open a bit longer compared to polling. The server **doesn’t return an empty response**.

The upside of using this technique is that there are **fewer requests** sent from the client to the server than the regular polling mechanism. This cuts down a lot of **network** **bandwidth** consumption.

<img width="696" alt="image" src="https://user-images.githubusercontent.com/47337188/164861591-ac17b74e-c48b-4b71-95c9-a48cf84070d6.png">



* Server-Sent Events (HTML5 Event-Source API)

The Server-Sent Events (SSE) implementation takes a different approach. Instead of the client polling for data, the server automatically pushes the data to the client whenever the updates are available. The incoming messages from the server are treated as **events.**

Via this approach, the servers can initiate data transmission towards the client once the client has established the connection with an **initial request.**

An important thing to note here is that once the client establishes a connection with the server, the data flow is in **one direction** only, from the server to the client.

SSE is ideal for scenarios like a real-time Twitter **feed**, displaying stock quotes on the UI, real-time notifications, etc.



* Streaming over HTTP (HTML5 and a JavaScript Stream API)

Streaming over HTTP is ideal for cases where we need to stream extensive data over **HTTP** by breaking it into **smaller chunks**.

The technique is primarily used for streaming **multimedia** content, like large images, videos, etc., over HTTP. Empowered by this technique, we can watch a **partially downloaded video** as it downloads by playing the downloaded chunks on the client.


## References

https://www.educative.io/module/web-application-architecture-101
