# Containerization
Containerization is the packaging of software code with just the operating system (OS) libraries and dependencies required to run the code to create a single lightweight executable—called a container—that runs consistently on any infrastructure.

More portable and resource-efficient than virtual machines (VMs), containers have become the de facto compute units of modern cloud-native applications.

Perhaps most important, containerization allows applications to be “written once and run anywhere.” This portability speeds development, prevents cloud vendor lock-in and offers other notable benefits such fault isolation, ease of management, simplified security and more.

The concept of containerization and process isolation is actually decades old, but the emergence in 2013 of the open source Docker Engine.

## Intro

### Layers of Containerization
Let’s take a closer look at how all the pieces — from hardware to the containerized application — fit together.

- **Hardware infrastructure**: With any application, it all starts with physical compute resources somewhere. Whether those resources are your own laptop or spread across multiple cloud datacenters, they are a must-have for containers to work.
- **Host operating system**: The next layer that sits atop the hardware layer is the host operating system. As with the hardware layer, this could be as simple as the Windows or *nix operating system running on your own computer or abstracted away completely by a cloud service provider.
- **Container engine**: This is where things start to get interesting. Container engines run on top of your host operating system and virtualize resources for containerized apps. The simplest example of this layer is running Docker on your own computer.
- **Containerized apps**: Containerized apps are units of code that include all the libraries, binaries, and configuration an application requires to run. A containerized application is run as an isolated process in “user space” (outside of the operating system’s kernel).

### vs. Virtualization
It’s easy for the uninitiated to be confused by the difference between containerization (what containerization software like Docker enables) and traditional server virtualization (what hypervisors like HyperV and VMware ESXi enable). In simple terms, the difference boils down to this:
- Server virtualization is about abstracting hardware and running an operating system. Containerization is about abstracting an operating system and running an app.
- They both abstract away resources, containerization is just another level “up” from server virtualization. In fact, containerization and server virtualization aren’t mutually exclusive. You can run containerized apps on top of a container engine that is deployed within a virtual machine.

### Use Cases
- **Microservices**: A microservice architecture is built around the idea of many small, independent, and loosely coupled services working together. Because containers are a great way to deploy isolated units of code, they have become the de-facto standard for deploying microservices.
- **CI/CD**: Continuous integration/continuous deployment (CI/CD) is all about testing and deploying reliable software fast. By bundling applications into portable, lightweight, and uniform units of code, containerization enables better CI/CD because containers are automation friendly, reduce dependency issues, and minimize resource consumption.
- **Modernizing legacy apps**: Many teams are moving legacy monolithic applications to the cloud. However, in order to do so, they need to be sure the app will actually run in the cloud. In many cases, this means leveraging containerization to ensure the app can be deployed anywhere.

## Containers
Containers are lightweight packages of your application code together with dependencies such as specific versions of programming language runtimes and libraries required to run your software services.

Containers are often referred to as “lightweight,” meaning they share the machine’s operating system kernel and do not require the overhead of associating an operating system within each application.

### Types of Containers

**System containers (Linux containers - LXC)**

They run a full operating system inside them, you can run any type of workload, and you manage them exactly as you would a virtual or a physical machine.

**Application/process containers (Docker)**

Containers that package and run a single process or a service per container

They run stateless types of workloads that are meant to be ephemeral.

This means that these containers are temporary, and you can create, delete and replace containers easily as needed.

### Container Orchestration
Container orchestration is the automation of the deployment, management, scaling, and networking of containers.

Kubernetes, also known as K8s, is a popular container orchestration tool. There are other container orchestration tools, like Apache Mesos and Docker Swarm.

## Case Study: The Evolution of Container Usage at Netflix

Titus: Netflix’s infrastructural foundation for container based applications.

![image](https://user-images.githubusercontent.com/47337188/185522842-6c594464-3734-4aa1-91e2-a8dc65bfcec4.png)

Titus supports both service jobs that run “forever” and batch jobs that run “until done”.

Service jobs restart failed instances and are autoscaled to maintain a changing level of load.

Batch jobs are retried according to policy and run to completion.


## *References
https://www.checkpoint.com/cyber-hub/cloud-security/what-is-container-security/what-is-containerization/

https://www.ibm.com/cloud/learn/containerization

https://cloud.google.com/learn/what-are-containers

https://earthly.dev/blog/lxc-vs-docker/

https://netflixtechblog.com/the-evolution-of-container-usage-at-netflix-3abfc096781b



