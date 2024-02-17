# Docker Study

## Client/Server Model

It’s easiest to think of Docker as consisting of two parts: the client and the server/daemon. Optionally there is a third component called the registry, which stores Docker images and their metadata.

![image](https://user-images.githubusercontent.com/47337188/187095815-89e5c9de-2a45-4057-86f5-0fa541f63fd8.png)

A container is an instance of an image. Whenever we need to run a particular image, we need to have that image on the system.

Using the Docker client, you can ask the Docker daemon to run a particular image.

The daemon will go ahead and look for the image on a system. If it finds the image, it will run the container forked from that image. However, if the image is not present on the system, it will pull the image from the Docker registry and create a container from the image.


## Manage Data

By default all files created inside a container are stored on a writable container layer.

This means that:
- The data doesn’t persist when that container no longer exists, and it can be difficult to get the data out of the container if another process needs it.
- A container’s writable layer is tightly coupled to the host machine where the container is running. You can’t easily move the data somewhere else.
- Writing into a container’s writable layer requires a storage driver to manage the filesystem. The storage driver provides a union filesystem, using the Linux kernel.

![image](https://user-images.githubusercontent.com/47337188/187097813-1edd8c4e-2220-43c1-96c5-70308c06d23d.png)

(where the data lives on the Docker host differs)

Docker has two options for containers to store files on the host machine, so that the files are persisted even after the container stops: volumes, and bind mounts.

Docker also supports containers storing files in-memory on the host machine.  Such files are not persisted. If you’re running Docker on Linux, tmpfs mount is used to store files in the host’s system memory.

No matter which type of mount you choose to use, the data looks the same from within the container. It is exposed as either a directory or an individual file in the container’s filesystem.

## Dockerfile
Docker can build images automatically by reading the instructions from a Dockerfile

A Dockerfile is a text document that contains all the commands a user could call on the command line to assemble an image.

A Docker image consists of read-only layers each of which represents a Dockerfile instruction.

The layers are stacked and each one is a delta of the changes from the previous layer.

## Layers

### Image Layers
Each of the files that make up a Docker image is known as a layer.

These layers form a series of intermediate images, built one on top of the other in stages, where each layer is dependent on the layer immediately below it.

The hierarchy of your layers is key to efficient lifecycle management of your Docker images.

### Container Layers
Each time Docker launches a container from an image, it adds a thin writable layer, known as the container layer, which stores all changes to the container throughout its runtime.

This layer is the only difference between a live operational container and the source Docker image itself.

<img width="500" alt="image" src="https://user-images.githubusercontent.com/47337188/188183517-be886f62-6730-4315-a0db-a4b7c1c61c43.png">

### Container Orchestration 
Kubernetes and Docker Compose are both container orchestration frameworks. Kubernetes runs containers over a number of computers, virtual or real. Docker Compose runs containers on a single host machine.

![image](https://user-images.githubusercontent.com/47337188/188191851-e3196837-163f-49c5-8f70-3a4b8480ceec.png)

With Docker Compose, you use a YAML file to configure your application’s services. Then, with a single command, you create and start all the services from your configuration.

**Kubernetes**

Containers are organized into an abstraction called a pod. A pod can have one or many containers.

A pod’s logic is exposed to the network by way of another Kubernetes abstraction called a service.

In short, the network knows about Kubernetes services and a service knows about the pod(s) that has its logic. Within each pod is one or many containers that realize the logic in the given pod.

![image](https://user-images.githubusercontent.com/47337188/188192406-b39c776b-0376-4c53-8d4a-bc916c5fe026.png)

Under Kubernetes, containers, pods, and services are hosted within a collection of one or many computers, real or virtual.

Kubernetes runs over a number of nodes. The collection of nodes is called a Kubernetes cluster.

Pods and the containers associated with a service can be hosted over a number of machines.

Kubernetes has scaling and fault-tolerance features. Docker Compose supports automatic restarts on failure but is not intended to support auto-scaling.

Even though Kubernetes is most commonly used with Docker, but it can also be used with any container runtime.

## *References
https://docs.docker.com/

https://jfrog.com/knowledge-base/a-beginners-guide-to-understanding-and-building-docker-images/

https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/What-is-Kubernetes-vs-Docker-Compose-How-these-DevOps-tools-compare#:~:text=Kubernetes%20and%20Docker%20Compose%20are,on%20a%20single%20host%20machine.
