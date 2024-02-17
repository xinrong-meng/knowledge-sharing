# Data Lake

A data lake can include structured data from relational databases (rows and columns), semi-structured data (CSV, logs, XML, JSON), unstructured data (emails, documents, PDFs) and binary data (images, audio, video).

A data lake can be established "on premises" (within an organization's data centers) or "in the cloud" (using cloud services from vendors such as Amazon, Microsoft, or Google).

Poorly managed data lakes have been facetiously called data swamps.

**<> Data warehouse**

Data lakes were developed in response to the limitations of data warehouses. While data warehouses provide businesses with highly performant and scalable analytics, they are expensive and proprietary and can’t handle the modern use cases most companies are looking to address. Data lakes are often used to consolidate all of an organization’s data in a single, central location, where it can be saved “as is,” without the need to impose a schema (i.e., a formal structure for how the data is organized) up front like a data warehouse does.

**Why**

First and foremost, data lakes are open format, so users avoid lock-in to a proprietary system like a data warehouse, which has become increasingly important in modern data architectures.

Data lakes are also highly durable and low cost, because of their ability to scale and leverage object storage. Additionally, advanced analytics and machine learning on unstructured data are some of the most strategic priorities for enterprises today. The unique ability to ingest raw data in a variety of formats (structured, unstructured, semi-structured), along with the other benefits mentioned, makes a data lake the clear choice for data storage.

**Challenges**

Despite their pros, many of the promises of data lakes have not been realized due to the lack of some critical features: no support for transactions, no enforcement of data quality or governance, and poor performance optimizations.

## Origin

In October of 2010, James Dixon, founder and former CTO of Pentaho, came up with the term "Data Lake".

Many business applications are essentially state machines. State machines are very good at answering questions about the state of things. But what about reporting on trends and changes over the short and long term? How do we do this? The answer for this is to track changes to the attributes in change logs.

These change logs are database tables or text files that list the changes made over time. That way you can (although the data transformation is ugly) rewind the change log of a specific field across all objects in the system and then aggregate those changes to get a view over time. This is not easy to do and assumes that you have a change log.

Typically, change logs only exist for the main fields in an application. There might only be change logs on 10-20% of the fields. So if you suddenly have an impulse so see how a lesser attribute has changed over time you are out of luck. It is impossible because that information is lost.

The Data Lake approach solves this problem. You store all of the data in a Data Lake, populate data marts and your data warehouse to satisfy traditional needs, and enable ad-hoc query and reporting on the raw data in the Data Lake for new questions.

Now we have the initial state of the application’s data and the changes to of all of the attributes, not just the main/traditional fields. We can apply this approach to more than one application, each with its own Data Lake of state logs, storing every incremental change and event. So now we have the state of every field of (potentially) every business application in an enterprise across time. We have the “Union of the State”.

What are the potential use cases for the Union of the State?

**Enterprise Time Machine**

In order to reconstruct the state at any point in time we need to load the initial snapshot into a repository and then update the attributes of each object as we process the logs, event by event, until we get to the point in time that we are interested in. A NoSQL store such as MongoDB , HBase, or Cassandra should work well as the repository. This process could be optimized by adding regular snapshots of the whole state into the Data Lake so that we don’t have to process from the very beginning every time.

**Trending**

Since we can re-create the state at any point in time we can do trending and historical analysis of any and every attribute over any time period, at any time granularity we want.

### Architecture

- Let the application store it’s current state in a relational or No-SQL repository. Don’t affect the operation of the operational system.
- Log all events and state changes that occur within the application.
- Provide the ability to rewind the state of any and all attributes by parallel processing of the logs.
- Provide the facilities listed above using technologies appropriate of each use case (using the rewind capability).

### In a nutshell

Most of the applications in use capture the state of the enterprise in some way.

A fraction of the changes to the state are captured via change logs.

Dixon suggests to store all of enterprise data in a data lake and effectively create change logs for every field.

In addition, Dixon suggests to capture behavioral data for how applications of all types were used.

In this way the data lake comes a time machine that allows the state of the enterprise at any one moment to be captured and analyzed.

The power to see what happened before and after important events will lead to even better predictive models and a deeper understanding of operations.

## *References
https://en.wikipedia.org/wiki/Data_lake

https://jamesdixon.wordpress.com/2015/01/22/union-of-the-state-a-data-lake-use-case/

https://www.forbes.com/sites/danwoods/2015/01/26/james-dixon-imagines-a-data-lake-that-matters/?sh=6e73fdfb4fdb

https://www.databricks.com/discover/data-lakes/introduction


