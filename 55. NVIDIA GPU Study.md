# NVIDIA GPU Study

## NVIDIA Deep Learning Software Stack

<img width="800" alt="image" src="https://user-images.githubusercontent.com/47337188/235309778-edf1ff71-5fd2-42ef-91e4-21be53426241.png">

The **hardware** is comprised of a system which can be a workstation or a server with one or more GPUs.

The system is provisioned with an **operating system** and an **NVIDIA driver** that enables the **deep learning framework** to leverage the 
GPU functions for accelerated computing

**Containers** are becoming the choice for development in organizations. NVIDIA provides many frameworks as Docker 
containers through NGC, which is a Cloud Registry for GPU accelerated software.
It hosts over 100 containers for GPU accelerated applications, tools, and frameworks. These containers help with 
faster and more portable development and deployment of **AI applications** on GPUs across the Cloud, data center, etc 
and are optimized for accelerated computing on GPUs. Hence, the stack includes running the **NVIDIA Docker 
Runtime** specific for NVIDIA GPUs. The containers include all the required libraries to deliver high performance GPU 
acceleration during the processing required for training.

The **CUDA toolkit** is an NVIDIA groundbreaking parallel programming model that performs essential optimizations for deep learning, machine learning, and high performance 
computing, leveraging NVIDIA GPUs.

## Compute Unified Device Architecture - CUDA

CUDA® is a parallel computing platform and programming model developed by NVIDIA for general computing on graphical 
processing units (GPUs). With CUDA, developers are able to dramatically speed up computing applications by 
harnessing the power of GPUs.

In GPU-accelerated applications, the sequential part of the workload runs on the CPU – which is optimized for 
single-threaded performance – while the compute intensive portion of the application runs on thousands of GPU cores 
in parallel.

When using CUDA, developers program in popular languages such as C, C++, Fortran, Python and MATLAB and express 
parallelism through extensions in the form of a few basic keywords.

### vs. Open Computing Language - OpenCL

**Vendor Support**

CUDA is developed by NVIDIA and is primarily designed for use with NVIDIA GPUs, while OpenCL is an open standard 
supported by a range of vendors, including NVIDIA, AMD, and Intel, and can be used with a variety of hardware, 
including CPUs, GPUs, and etc.

**Programming Model**

CUDA provides a low-level programming model that requires developers to write code specifically for NVIDIA GPUs, while OpenCL provides a higher-level programming model that can be used with a variety of hardware devices and is more flexible in terms of the programming language used.

**Performance**

CUDA is generally considered to provide better performance on NVIDIA GPUs, as it is specifically designed for use with these devices, while OpenCL is more flexible but may not provide optimal performance on all hardware platforms.

**Ecosystem**

CUDA has a large and well-established ecosystem, including a range of libraries and tools, while OpenCL 
has a smaller ecosystem but is supported by a range of vendors.

### CUDA Programming

The host is the CPU available in the system. The system memory associated with the CPU is called host memory. The 
GPU is called a device and GPU memory likewise called device memory.

To execute any CUDA program, there are three main steps:

- Copy the input data from host memory to device memory, also known as host-to-device transfer.
- Load the GPU program and execute, caching data on-chip for performance.
- Copy the results from device memory to host memory, also called device-to-host transfer.

## Common Uses of GPU Parallel Computing

**Computer graphics**

Startups and significant-tech companies use GPUs to create photo-realistic 3D graphics for games, movies, etc. GPUs allow for more detailed and realistic graphics than CPUs are capable of.

**Deep learning**

Deep learning has been used in various areas, including speech recognition, image recognition, and natural language 
processing.

**Data mining**

It is a way of discovering useful information from large amounts of data. GPUs make data mining faster and more efficient.

**Scientific computing**

It is used in fields like chemistry, biology, and physics. With GPU parallel computing, you can speed up simulations 
and modelings.

## Value of On-prem and Cloud Infrastructure

When deciding what platform to use at different stages of the development cycle, it's important to understand how 
cloud and on-prem approaches support these stages. For **initial stages** with smaller, less complex data sets, **cloud** 
compute instances backed by GPUs are ideal for early prototyping. However, as **data sets get larger and deep learning 
models become more complex**, it's better to deploy processing closer to where the data is located, which usually 
means bringing the training environment **on-premises**. This can help drive down costs, allow for faster iteration, and 
provide a fixed cost infrastructure managed by the IT department. It also helps them avoid potential concerns around 
data privacy.

A **hybrid** approach combining Cloud-hosted GPU resources for early experimentation and on-premises computing for 
large-scale deep learning training may be the best approach for most organizations.

## Reference

https://www.coursera.org/learn/introduction-to-ai-in-the-data-center/

https://developer.nvidia.com/cuda-zone

https://www.turing.com/kb/understanding-nvidia-cuda

https://developer.nvidia.com/blog/cuda-refresher-cuda-programming-model/

ChatGPT

