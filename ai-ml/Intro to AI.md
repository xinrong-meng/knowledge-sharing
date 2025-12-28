# Intro to AI

**AI** is a broad field of study focused on using computers to do things that require human level intelligence.

**Machine Learning**, ML is an approach to AI that uses statistical learning algorithms to build a model from observed data.

Let's consider a typical AI workflow. It is broken down into 3 fundamental process steps, each of which can be GPU accelerated. The first is data preparation.

<img width="873" alt="image" src="https://user-images.githubusercontent.com/47337188/235268101-06d3999a-3499-45da-ba2c-4deeddcfc205.png">

Once the data has been prepared accordingly, it is fed into a model. A machine-learning model is a data processing 
mechanism that has been trained to recognize certain types of patterns. The model is trained over a set of data by 
using a mathematical algorithm to process and learn from the data. Training is an iterative process. A model is not 
ready to deploy after just one training. Data scientists can iterate many times before producing a model that is 
ready for deployment. By multiplying the number of times training occurs, with the amount of time it takes to train. 
It is evidenced that processing speed is of utmost importance. With the advent of GPU accelerated machine learning, 
we can distribute model training across multiple GPUs and multiple nodes, but little or no latency.

### Deep Learning

**Deep Learning**, DL is a machine-learning technique that is inspired by how the human brain learns i.e. filtering the
input data through **layers** and predicting and classifying information. Most of the deep learning methods used **neural network** models.

<img width="300" alt="image" src="https://user-images.githubusercontent.com/47337188/236562044-43eb00fe-be2b-4237-8310-7026310ee9cb.png">

Consider an application that automatically identifies various types of animals. In other words, a **classification** 
task. The first step is to assemble a collection of representative examples to be used as a **training dataset**, which 
will serve as the experience from which a neural network will learn. If the classification is only cats versus dogs, 
then only cat and dog images are needed in the training dataset.

The next component that is needed is a deep neural network model. The word deep indicates that the neural network 
will have multiple layers.

There are **readily** available deep neural network models for image classification, object recognition, image 
segmentation, and several other tasks, but it is often necessary to **modify** these models to achieve high levels of 
accuracy for a particular dataset.

Once a training set has been assembled, and a neural network model selected, a **deep learning framework** is used to 
feed the training dataset through the neural network. Deep learning frameworks offer building blocks for designing, 
training, and validating deep neural networks through a high-level programming interface. For each image that is 
processed through the neural network, each node in the output layer reports a number that indicates how confident it 
is that the image is a dog or a cat. In this case, there are only two options, so the model needs just two nodes in 
the output layer, one for dogs and one for cats.

When these final outputs are sorted in a most confident to least confident manner, the result is called a confidence 
vector. The deep learning framework then looks at the label for the image to determine whether the neural network 
guessed or inferred the correct answer. If it inferred correctly, the framework strengthens the weights of the 
connections that contributed to getting the correct answer and vice versa. If the neural network inferred the 
incorrect result, the framework reduces the weights of the connections that contributed to getting the wrong answer.

## Graphics Processing Units

GPU, is a specialized electronic circuit designed to rapidly manipulate and alter memory to accelerate the creation 
of images in a frame buffer intended for output to a display device. Computer graphics have evolved significantly 
since the 1970s. Their importance is paramount due to humans using vision as the main means to consume the 
information that computers provide. Images on screens are comprised of picture elements or pixels. A pixel is the 
smallest unit of a digital image that can be displayed and represented on a digital display device. The 
characteristics of a pixel include position, color, and brightness. All the pixels that make up an image needs to be 
processed at such a rate that the human eye does not perceive any delays or inconsistencies as it absorbs the image 
being presented.

As display and computer technology has advanced, the number of pixels on a screen has increased, allowing for a more 
realistic representation of images. This is called the resolution of the screen, which represents pixel density. The 
processing behind the pixels is done by the GPU.

GPUs are designed to execute simple instruction sets. Consequently, the number of cores that can be built in a 
comparatively similar silicone area is much larger than with a CPU. With relatively many more cores than a CPU, a 
GPU allows processing many simple instructions simultaneously.

Both CPUs and GPUs are components of a system that work in tandem to process code and data.

A typical application has parts which needs to be executed sequentially and parts which can be executed in parallel. 
Although the parallel parts may only be a small part of the overall application, they're usually the most compute 
intensive and time-consuming. Therefore, by executing them in parallel on a GPU, we can see huge increases in 
performance.

## Reference

https://www.coursera.org/learn/introduction-to-ai-in-the-data-center/
