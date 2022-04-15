### Unbounded Data: Batch

Unbounded data can be processed by batch engines.

#### Fixed windows

Windowing the input data into **fixed-size** windows and then processing each of those windows as a **separate**, **bounded** data source.

Particularly for input sources like **logs**, for which events can be written into **directory** and **file** hierarchies whose **names** encode the **window** they correspond to.In reality, however, most systems still have a **completeness** problem. You may need to delay processing until you’re **sure** **all events** have been **collected** or **reprocessing** the entire batch for a given window whenever data arrives **late**.

![alt_text](https://user-images.githubusercontent.com/47337188/163653337-d348e0b8-3386-4863-8756-82b2236309d7.png "Fixed window")

#### Sessions

This approach breaks down even more.

Sessions are typically defined as **periods** of **activity** (e.g., for a specific **user**) terminated by a gap of inactivity.

Note that sessions may be **split across batches**, as indicated by the red marks. We can **reduce** the number of splits by increasing batch sizes or adding additional logic to stitch up sessions from previous runs.

![alt_text](https://user-images.githubusercontent.com/47337188/163653343-a13c178f-1cd4-4b20-9401-f9e9c928dabb.png "Session")

### Streaming System

Streaming data processing is important in **big data** because:
* lower latency
* massive, **unbounded** datasets
* process data as they arrive **spreads** **workloads** **out** more **evenly**, yielding more consistent and **predictable** **consumption** of **resources**.

Streaming system is a type of data processing engine that is designed with unbounded datasets in mind.

#### Two primary constitutions

**Tables** and **streams** are two primary constituents.

A **table** is a **holistic** view of a dataset at a specific **point** in **time**.

A **stream** is an **element-by-element** view of the evolution of a dataset **over time**.

**Streams → tables**: The **aggregation** of a **stream of updates** over time yields a **table** (~= WAL).

**Tables → streams**: The **observation** of **changes** to a table over time yields a **stream** (~= Materialized view).

#### Two domains of time

* Event Time

  This is the time at which events actually **occurred**.

* Processing Time

  This is the time at which events are **observed** in the system.

Event time and processing time would always be equal in an ideal world.

#### Windowing

Windowing is simply the notion of taking a data source (either unbounded or bounded), and **chopping** it **up** along temporal boundaries into finite **chunks** for processing.

3 different patterns

![alt_text](https://user-images.githubusercontent.com/47337188/163653349-a5eba358-ffb4-4bc9-adac-7457ec015664.png "Window patterns")

#### Triggers

A trigger is a mechanism for declaring **when** the **output for a window** should be **materialized** relative to some external signal.

In some sense, you can think of them as a **flow control **mechanism for dictating when results should be materialized. Another way of looking at it is that triggers are like the shutter-release on a camera, allowing you to declare when to **take snapshots** in time of the results being computed.

#### Watermarks

A watermark is a notion of **input** **completeness** with respect to **event times**.

A watermark with value of time X makes the statement: “all input data with event times less than X have been observed.”

![alt_text](https://user-images.githubusercontent.com/47337188/163653355-9168183b-5dde-4875-b2f9-faaefc82654d.png "Watermark")

The **red line** representing reality is the **watermark**.

Conceptually, you can think of the watermark as a function, `F(P) → E`, which takes a point in processing time and returns a point in event time. That point in event time, `E`, is the point up to which the system believes all inputs with event times less than `E` have been observed.

There are two types of watermarks:

* Perfect watermarks

For the case in which we have perfect knowledge of all of the input data, it’s possible to construct a perfect watermark. In such a case, there is **no** such thing as **late data**; all data are **early or on time**.

* Heuristic watermarks

For many distributed input sources, **perfect** knowledge of the input data is **impractical**, in which case the next best option is to provide a heuristic watermark. Heuristic watermarks use whatever information is available about the inputs (partitions, ordering within partitions if any, growth rates of files, etc.) to provide an **estimate** of progress that is as accurate as possible.The use of a heuristic watermark means that it might sometimes be wrong, which will lead to **late data**.

#### Accumulation

An **accumulation mode** specifies the **relationship** between **multiple** **results** that are observed **for the same window**.

There are three accumulation modes:

* **Discarding** (in which results are all **independent** and distinct)

  Every time a pane is materialized, any **stored state** is **discarded**.

  This means that each successive pane is independent from any that came before.

  Discarding mode is useful when the **downstream** consumer is performing some sort of **accumulation** itself; for example, when sending integers into a system that expects to receive deltas that it will sum together to produce a final count.

* **Accumulating** (in which later results **build upon** prior ones)

  Every time a pane is materialized, any **stored state** is **retained**, and future inputs are accumulated into the existing state.

* **Accumulating** and **retracting**

  **Retractions** (**combined** with the new **accumulated** **result**) are essentially an explicit way of saying “I previously told you the result was X, but I was wrong. Get rid of the X I told you last time, and replace it with Y.”

  When consumers downstream are regrouping data by a different dimension, it’s entirely possible the new value may end up keyed differently from the previous value and thus end up in a **different group**. In that case, the new value can’t just overwrite the old value; you instead need the retraction to **remove the old value.**

Let’s compare accumulation modes:
![alt_text](https://user-images.githubusercontent.com/47337188/163653360-b23f23ac-bd17-432c-972f-109fc3545da3.png "Accumulation modes")

### References
Streaming Systems By Tyler Akidau, Slava Chernyak, Reuven Lax