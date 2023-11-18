# Concurrency in Practice

## 1. Challenges

| Challenge       | Description                                                                                   | Solutions                                                                                                                  |
|-----------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Race Conditions | Occurs when multiple threads modify shared data concurrently without synchronization.        | - Use mutexes/locks*.<br>- Atomic operations.<br>- Immutability.<br>- Thread-local storage.                                 |
| Deadlocks       | Happens when two or more threads are waiting for each other to release resources, causing a halt in execution. | - Impose lock ordering*.<br>- Lock timeouts.<br>- Deadlock detection algorithms.<br>- Resource hierarchy.                  |
| Starvation      | Occurs when one or more threads are perpetually denied access to resources they need.         | - Fair locks/scheduling*.<br>- Priority inversion prevention.<br>- Resource allocation guarantees.<br>- Load balancing.     |

**Use mutexes/locks Example**
```python
import threading

counter = 0
lock = threading.Lock()

def inc_counter():
    global counter
    for _ in range(100):
        lock.acquire()
        try:
            counter += 1
        finally:
            lock.release()
 
threads = [threading.Thread(target=inc_counter) for _ in range(10)]

for thread in threads:
   thread.start()
 
for thread in threads:
   thread.join()

print(f"Value of counter: %s" % counter)
```

**Impose lock ordering Example**
```python
import threading

resource_a = 'A'
resource_b = 'B'
lock_a = threading.Lock()
lock_b = threading.Lock()

global_lock_order = [lock_a, lock_b]

def process_one():
    with lock_a:
        print("Process One has acquired lock on Resource A")
        with lock_b:
            print("Process One has acquired lock on Resource B")

    print("Process One has released locks on Resource A and B")

def process_two():
    with lock_a:
        print("Process Two has acquired lock on Resource A")
        with lock_b:
            print("Process Two has acquired lock on Resource B")

    print("Process Two has released locks on Resource A and B")


thread_one = threading.Thread(target=process_one)
thread_two = threading.Thread(target=process_two)

thread_one.start()
thread_two.start()

thread_one.join()
thread_two.join()
```

**Fair locks/scheduling Example**
```python
import threading
import queue
import time

fair_queue = queue.Queue()

def access_resource(thread_id):
    # Simulate acquiring the lock
    fair_queue.put(thread_id)
    
    while fair_queue.queue[0] != thread_id:
        time.sleep(0.01)  # Sleep a bit to prevent busy waiting

    print(f"Thread {thread_id} is accessing the shared resource.")
    time.sleep(0.5)  # Simulate some work with the resource
    
    # Simulate releasing the lock
    fair_queue.get()
    print(f"Thread {thread_id} has finished accessing the shared resource.")


threads = [threading.Thread(target=access_resource, args=(i,)) for i in range(5)]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
```

## 2. Immutability

The key concern in concurrent programming is shared mutable state, which can lead to complex synchronization issues 
and bugs.

Immutability refers to the state of an object being unchangeable after its creation. In other words, once an object 
is created, its state cannot be modified. If you need a modified version of the object, you create a new object with 
the desired state.

The results of these operations (i.e., the new objects) are not uniform across all 
threads, as each operation is independent. One thread's operations do not affect another's.

Each thread may have its own view of the data, based on its operations. These views are 
consistent within the thread but are not intended to be uniform across all threads.

## 3. Task Scheduling and Execution

Task queues and thread pools are often used together in concurrent programming to manage and execute tasks efficiently.

The task queue holds the tasks, and the thread pool supplies the threads that process these tasks. When a thread in
the pool becomes available, it picks a task from the queue and executes it.

Imagine a web server handling HTTP requests. Each request can be considered a task. These tasks are placed in a task
queue. The server has a thread pool with a fixed number of threads. Each thread takes a request from the queue and
processes it (e.g., fetching data, performing computations). This way, the server can handle multiple requests
concurrently, using a limited number of threads, and manage incoming requests efficiently without overwhelming the
system resources.

### Thread Pools

A thread pool is a collection of pre-instantiated reusable threads. These threads are used to execute tasks.

Thread pools are used to manage the thread lifecycle efficiently, limit the number of active threads, and reduce the
overhead associated with thread creation and destruction.

**Example**
```python
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# A simple function that simulates a task
def perform_task(task_number):
    print(f"Starting task {task_number}")
    time.sleep(2)  # Simulating a task taking some time
    print(f"Task {task_number} completed")
    return f"Result of task {task_number}"


with ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(perform_task, i) for i in range(5)]

    for future in as_completed(futures):
        print(future.result())


print("All tasks completed.")
```

### Task Queues

A task queue is used to store and manage tasks that are waiting to be executed. It acts as a buffer between task
producers (who submit tasks) and consumers (who execute tasks).

This example below demonstrates how to use a thread pool in combination with a task queue to process a set of tasks.

**Example**
```python
import concurrent.futures
import queue
import time

def process_task(task):
    print(f"Processing task: {task}")
    time.sleep(1)

def add_tasks_to_queue(task_queue, num_tasks):
    for task in range(num_tasks):
        task_queue.put(task)
    for _ in range(num_workers):  # Add None entries to signal the end of tasks
        task_queue.put(None)

def worker(task_queue):
    while True:
        task = task_queue.get()
        if task is None:  # Signal to stop the worker
            break
        process_task(task)

num_tasks = 10
num_workers = 3

task_queue = queue.Queue()
add_tasks_to_queue(task_queue, num_tasks)

with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    futures = [executor.submit(worker, task_queue) for _ in range(num_workers)]
    concurrent.futures.wait(futures)

print("All tasks have been processed.")
```

## 4. Thread Signaling

Proper thread signaling in concurrent programming is crucial for coordinating the actions of multiple threads. It
involves using specific mechanisms to signal between threads, allowing them to efficiently communicate about the
state of shared resources or the progress of tasks.

| Method            | Usage                                          | Mechanism                                                                                     | Typical Use Cases                                  |
|-------------------|------------------------------------------------|-----------------------------------------------------------------------------------------------|----------------------------------------------------|
| Condition Variables* | Synchronize threads based on certain conditions | Threads wait on a condition variable. When a condition changes, another thread signals it.   | Waiting for specific states or conditions to be met in shared data. |
| Semaphores*        | Control access to resources; signaling         | A counter controls access. Threads increment/decrement it. If zero, threads wait.             | Limiting access to a resource; simple signaling.   |
| Event Objects     | Signal state changes or events                 | An event with a boolean flag. Threads wait for the flag to be set.                            | One-time signals like start/stop events.           |
| Message Queues    | Communicate data between threads               | Threads send and receive messages through a queue.                                            | Complex data exchange; producer-consumer patterns. |
| Barriers*          | Synchronize a set of threads at a point        | Threads wait at a barrier until all have reached it, then proceed.                            | Synchronizing phases in parallel algorithms.       |

**Condition Variables Example**
```python
import threading

condition = threading.Condition()
item = None

def producer():
    global item
    with condition:
        item = "Something"
        condition.notify()

def consumer():
    with condition:
        condition.wait()
        print(f"Consumed: {item}")

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

consumer_thread.start()
producer_thread.start()

consumer_thread.join()
producer_thread.join()
```
The producer function sets the item and then notifies the condition variable. The consumer function waits for the
condition variable to be notified. Once notified, it proceeds to consume the item. `with condition:` is a context
manager that acquires and releases the underlying lock associated with the condition variable.

**Semaphores Example**
```python
import threading

semaphore = threading.Semaphore(0)
item = None

def producer():
    global item
    item = "Something"
    semaphore.release()

def consumer():
    semaphore.acquire()
    print(f"Consumed: {item}")

producer_thread = threading.Thread(target=producer)
consumer_thread = threading.Thread(target=consumer)

consumer_thread.start()
producer_thread.start()

consumer_thread.join()
producer_thread.join()
```

The semaphore is initialized with a count of 0, which means any call to acquire() will block until release() is called.
The consumer thread waits (blocks) on semaphore.acquire(). The producer thread, after producing an item, calls
semaphore.release(), which increments the semaphore count and unblocks the consumer.

**Barriers Example**
```python
import threading

barrier = threading.Barrier(2)

def task():
    print(f"Task waiting at barrier. Thread ID: {threading.get_ident()}")
    barrier.wait()
    print("Barrier crossed.")

thread1 = threading.Thread(target=task)
thread2 = threading.Thread(target=task)

thread1.start()
thread2.start()

thread1.join()
thread2.join()
```

A barrier is created for two threads. Each task thread prints a message, waits at the barrier with barrier.wait(),
and then prints another message after crossing the barrier. The barrier makes both threads wait until both have
reached the barrier.wait() call. Once both threads have reached this point, they are both released to continue.

## 5. <  > Asynchronous Programming

Asynchronous programming allows a single thread to handle multiple tasks without blocking the execution flow, 
especially useful for I/O-bound operations. This is achieved through a mechanism that involves an event loop and 
non-blocking calls.

The core concept in asynchronous programming is the event loop. This is a construct that waits for and dispatches 
events or messages in a program. It runs continuously to check for tasks that need to be executed.

In a synchronous program, when an I/O operation (like reading from a file, making a network request) is initiated, 
the program execution is blocked until the operation completes. In contrast, an asynchronous program makes 
non-blocking calls. This means when an I/O operation is initiated, the program doesn't wait for it to complete and 
can continue executing other code.

| Aspect                   | Asynchronous Programming                                      | Multi-threading                                               |
|--------------------------|---------------------------------------------------------------|---------------------------------------------------------------|
| **Nature**               | Event-driven, often single-threaded                           | Multiple threads of execution, potentially on multiple cores   |
| **Ideal for**            | I/O-bound tasks (network, file I/O)                           | CPU-bound tasks, parallel computations                        |
| **Concurrency Model**    | Non-blocking tasks, single-threaded event loop                | Multiple threads running in parallel                          |
| **Synchronization**      | Typically no traditional locks, relies on event loop          | Uses locks, mutexes, semaphores for shared resources          |
| **Thread Management**    | Managed by the event loop, minimal thread usage               | Thread pools manage and reuse worker threads                   |
| **Blocking Operations**  | Non-blocking by nature, tasks yield to the event loop         | Blocking operations can be offloaded to separate threads      |
| **Complexity & Overhead**| Lower complexity for I/O tasks, async/await pattern           | Higher complexity due to thread management and synchronization|
| **Use Case Example**     | Handling many concurrent network requests                     | Performing complex calculations across multiple CPU cores     |

**Example**
```python
import asyncio

async def simulate_long_running_task(name, duration):
    print(f"Task {name} started, it will take {duration} seconds.")
    await asyncio.sleep(duration)
    print(f"Task {name} finished.")

async def main():
    # Schedule multiple coroutines to run concurrently
    await asyncio.gather(
        simulate_long_running_task("A", 3),
        simulate_long_running_task("B", 2),
        simulate_long_running_task("C", 1)
    )

asyncio.run(main())
```

In the example with multiple coroutines using `asyncio.gather`, all coroutines are executed in the same thread. When 
one coroutine reaches an await (like await asyncio.sleep(duration)), it effectively tells the event loop, "I'm going 
to be idle for a while, go ahead and run other tasks." The event loop then switches to other coroutines and makes 
progress there.

**Coroutine**

These are special functions that can pause and resume their execution. Unlike traditional functions that
run from start to finish in one go, coroutines can be suspended at await expressions, allowing other coroutines to run.


**Coroutine Context**

Within the context of a single coroutine, `await` pauses the execution of that coroutine until the 
awaited task is complete. This could be seen as "blocking" within the local context of the coroutine.


**Event Loop Context**

From the perspective of the asyncio event loop, await is non-blocking. The event loop can 
continue doing other work while a coroutine is suspended due to an `await`.

## References

ChatGPT 4