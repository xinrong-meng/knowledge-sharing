# Data Warehouse
A data warehouse is a type of data management system that is designed to enable and support business intelligence (BI) activities, especially analytics.

Data warehouses are solely intended to perform queries and analysis and often contain large amounts of historical data.

The data within a data warehouse is usually derived from a wide range of sources such as application log files and transaction applications.

Data warehousing implements the process to 
- access heterogeneous data sources;
- clean, filter, and transform the data;
- and store the data in a structure that is easy to access, understand, and use.

The data is then used for query, reporting, and data analysis.

## Origin
The origin of the concept of data warehousing can be traced back to the early 1980s,
when relational database management systems emerged as commercial products.

The foundation of the relational model with its simplicity, together with the query capabilities provided by the SQL language,
supported the growing interest in what then was called end-user computing or decision support.

To support end-user computing environments, data was extracted from the organization′s online databases and stored in newly created database systems
dedicated to supporting ad hoc end-user queries and reporting functions of all kinds. One of the prime concerns underlying the creation of these systems was
the performance impact of end-user computing on the operational data processing systems. This concern prompted the requirement to separate end-user computing systems from transactional processing systems.

In those early days of data warehousing, the extracts of operational data were
usually snapshots or subsets of the operational data.

Data models for these decision support systems typically matched the
data models of the operational systems because, after all, they were extracted
snapshots anyhow.

One of the frequently occurring remodeling issues then was
to ″normalize″ the data to eliminate the nasty effects of design techniques that
had been applied on the operational systems to maximize their performance

The role and purpose of data warehouses in the data processing industry have
evolved considerably since those early days and are still evolving rapidly.

## Structuring the Data
In structuring the data, for data warehousing, we can distinguish three basic
types of data:

- Real-time data
- Derived data
- Reconciled data

**Real-time data**
Real-time data represents the current status of the business. It is typically used
by operational applications to run the business and is constantly changing as
operational transactions are processed.

To use real-time data in a data warehouse, typically it first must be cleansed to
ensure appropriate data quality, perhaps summarized, and transformed into a
format more easily understood and manipulated by business analysts. This is
because the real-time data contains all the individual, transactional, and detailed
data values as well as other data valuable only to the operational systems that
must be filtered out. In addition, because it may come from multiple different
systems, real-time data may not be consistent in representation and meaning.
As an example, the units of measure, currency, and exchange rates may differ
among systems. These anomalies must be reconciled before loading into the
data warehouse.

**Derived data**

Derived data is data that has been created perhaps by summarizing, averaging,
or aggregating the real-time data through some process.

Considering the requirements for improved query processing capability, an
efficient approach is to precalculate derived data elements and summarize the
detailed data to better meet user requirements.

**Reconciled Data**

Reconciled data is real-time data that has been cleansed, adjusted, or enhanced
to provide an integrated source of quality data that can be used by data analysts.

## Componnets
A typical data warehouse often includes the following elements:

- A relational database to store and manage data
- An extraction, loading, and transformation (ELT) solution for preparing the data for analysis
- Statistical analysis, reporting, and data mining capabilities
- Client analysis tools for visualizing and presenting data to business users
- Other, more sophisticated analytical applications that generate actionable information by applying data science and artificial intelligence (AI) algorithms, or graph and spatial features that enable more kinds of analysis of data at scale

**Different from OLTP systems**

<img width="795" alt="image" src="https://user-images.githubusercontent.com/47337188/190804196-480a7d22-6602-4fc3-8db4-c5c67e477047.png">

## Benefits
- Subject-oriented. They can analyze data about a particular subject or functional area (such as sales).
- Integrated. Data warehouses create consistency among different data types from disparate sources.
- Nonvolatile. Once data is in a data warehouse, it’s stable and doesn’t change.
- Time-variant. Data warehouse analysis looks at change over time.

## References
http://eddyswork.synthasite.com/resources/Data%20Modeling%20Tech%20For%20Data%20Warehouseing.pdf
https://www.oracle.com/database/what-is-a-data-warehouse/
