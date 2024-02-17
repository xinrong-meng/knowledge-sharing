# Data Transformation in Practice

## Data Storage and Management Systems

| Feature / Concept | Relational Databases | NoSQL Databases | Data Warehouses | Data Lakes |
|-------------------|----------------------|-----------------|-----------------|------------|
| **Data Types** | Structured data (tables with rows and columns). | Structured, semi-structured, and unstructured data. | Primarily structured data, optimized for analytics. | Structured, semi-structured, and unstructured data in raw form. |
| **Schema** | Schema-on-Write (fixed schema). | Schema-on-Read (flexible schema). | Schema-on-Write (fixed schema, often complex for analytics). | Schema-on-Read (no predefined schema). |
| **Use Cases** | OLTP (Online Transaction Processing), real-time data access, and management. | Large-scale, flexible applications; real-time analytics; IoT; content management. | OLAP (Online Analytical Processing), business intelligence, reporting, and complex queries. | Big data analytics, machine learning, data discovery, and historical data analysis. |
| **Scalability** | Vertically scalable (limited compared to NoSQL). | Highly scalable, both horizontally and vertically. | Scalable but can be expensive; cloud-based solutions offer more flexibility. | Extremely scalable, especially in cloud-based environments. |
| **Query Language** | SQL (Structured Query Language). | Varies (document, key-value, graph, column-family models). | SQL and extensions for analytics. | Requires big data processing tools (e.g., Hadoop, Spark) for querying. |
| **Data Integrity** | High (ACID properties). | Varies; some support ACID transactions, others prioritize performance and scalability. | High (ACID properties, especially in traditional setups). | Not typically focused on ACID properties; more about storage and analysis. |
| **Performance** | Optimized for transactional consistency and integrity. | Optimized for high throughput and flexibility. | Optimized for complex queries and aggregations. | Optimized for large-scale data processing and analytics. |
| **Storage Cost** | Moderate; depends on infrastructure. | Generally cost-effective due to flexibility in data storage. | Higher due to structured nature and processing capabilities. | Lower for raw data storage; costs associated with processing large datasets. |


## ETL < > ELT


| **Aspect**              | **ETL (Extract, Transform, Load)**                                                                  | **ELT (Extract, Load, Transform)**                                                              |
|-------------------------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------|
| **Process Flow**        | Data is extracted, transformed externally, and then loaded into the target system.                 | Data is extracted, loaded into the target system in raw form, and then transformed.             |
| **Data Transformation** | Transformation occurs before loading, typically in a separate processing area or tool.             | Transformation occurs after loading, within the data warehouse.                                 |
| **Computational Load**  | Requires separate computational resources for the transformation process.                          | Leverages the computational power of the data warehouse for transformation.                     |
| **Flexibility**         | Less flexible in adapting to changes as transformation logic is set during the ETL process.        | More flexible, as raw data is available in the warehouse, allowing for varied transformations.  |
| **Scalability**         | Scalability is limited by the capacity of the ETL processing environment.                          | Highly scalable, especially with cloud-based data warehouses that can handle large datasets.    |
| **Speed**               | Can be slower due to the separate transformation step before loading.                              | Often faster as data is quickly loaded and transformed using powerful data warehouse tools.      |
| **Storage Requirements**| Lower storage requirements in the data warehouse since data is stored post-transformation.         | Higher storage requirements as raw data is stored before transformation.                        |
| **Use Cases**           | Traditionally used in scenarios with limited data volume and computing power.                      | Ideal for big data scenarios and environments requiring high flexibility and scalability.        |
| **Technology Examples** | Traditional ETL tools like Talend.                                                                 | Modern data processing tools like dbt*, used in conjunction with cloud data warehouses.           |


## T(ransformation) Types

- **Basic Transformations**: Normalization, standardization, type conversion, and simple mathematical transformations.
- **Complex Transformations**: Pivot, transpose, and applying business logic.

Below is an example to demonstrate basic/complex transformations.
```shell
>>> wide_df = spark.createDataFrame([(1, 11, 1.1), (2, 12, 1.2)], ['id', 'int', 'double'])
>>> wide_df.show()
+---+---+------+
| id|int|double|
+---+---+------+
|  1| 11|   1.1|
|  2| 12|   1.2|
+---+---+------+
>>> long_df = wide_df.unpivot(ids='id', values=['int', 'double'], variableColumnName='type', valueColumnName='value')
>>> long_df.show()
+---+------+-----+
| id|  type|value|
+---+------+-----+
|  1|   int| 11.0|
|  1|double|  1.1|
|  2|   int| 12.0|
|  2|double|  1.2|
+---+------+-----+
>>> new_wide_df = long_df.groupBy('id').pivot(pivot_col='type', values=['int', 'double']).agg(first('value'))
>>> new_wide_df.show()
+---+----+------+
| id| int|double|
+---+----+------+
|  1|11.0|   1.1|
|  2|12.0|   1.2|
+---+----+------+
>>> new_wide_df.withColumn('int', col('int').cast('int')).show()
+---+---+------+
| id|int|double|
+---+---+------+
|  1| 11|   1.1|
|  2| 12|   1.2|
+---+---+------+
>>> wide_df.pandas_api().transpose().to_spark(index_col='new_id').show()
+------+----+----+
|new_id|   0|   1|
+------+----+----+
|    id| 1.0| 2.0|
|   int|11.0|12.0|
|double| 1.1| 1.2|
+------+----+----+
```
  

Define `df` as shown below to be used in the following examples.

```shell
>>> df = spark.createDataFrame([(1, 2), (3, 4), (5, None)], ["A", "B"])
>>> df.show()
+---+----+
|  A|   B|
+---+----+
|  1|   2|
|  3|   4|
|  5|NULL|
+---+----+
```

- **Aggregation**: Summarizing data (sums, averages, counts, max, min).

```shell
>>> df.agg({'A': 'sum', 'B': 'avg'}).show()
+------+------+
|sum(A)|avg(B)|
+------+------+
|     9|   3.0|
+------+------+
```

- **Filtering**: Removing unnecessary or irrelevant data.

```shell
>>> df.filter(df['A'] > 1).show()
+---+----+
|  A|   B|
+---+----+
|  3|   4|
|  5|NULL|
+---+----+
```

- **Joining and Merging**: Combining data from different sources.

```shell
>>> other_df = spark.createDataFrame([(1, 'a'), (2, 'b'), (3, 'c')], ['A', 'C'])
>>> other_df.show()
+---+---+
|  A|  C|
+---+---+
|  1|  a|
|  2|  b|
|  3|  c|
+---+---+

>>> joined_df = df.join(other_df, 'A')
>>> joined_df.show()
+---+---+---+
|  A|  B|  C|
+---+---+---+
|  1|  2|  a|
|  3|  4|  c|
+---+---+---+
```

- **Data Cleaning**: Handling missing values, smoothing noisy data, removing outliers, resolving inconsistencies.

```shell
>>> df.na.fill({'B': -1}).show()
+---+---+
|  A|  B|
+---+---+
|  1|  2|
|  3|  4|
|  5| -1|
+---+---+
```

## dbt (data build tool)

dbt enables data analysts and engineers to transform their data using the same practices that software engineers use 
to build applications.

### Manage Common Logic

dbt enables you to write SQL in a modular fashion. This improves maintainability and productivity because common 
logic can be consolidated (maintain a single instance of logic) and referenced (build on existing logic instead of 
starting from scratch).

The following figure is an example showing how dbt consolidates common logic. In this example, two models rely on 
the same subquery. Instead of replicating the subquery, dbt allows you to create a model for the subquery and 
reference it later.

![image](https://gist.github.com/assets/47337188/3369f4a8-f0c8-4461-b463-40ad295f1ee0)

The following is an example showing how dbt consolidates common logic related to fields. In this example, a model 
applies the same case statement on two fields. Instead of replicating the case statement for each field, dbt allows 
you to create a macro containing the case statement and reference it later.

![image](https://gist.github.com/assets/47337188/2497aae7-07cb-4109-9ebc-1b78f910dfa4)

### Manage Common Data Mappings

Although you can use macros to manage data mappings (for example, mapping “1” to “One” and “2” to “Two”), an alternative is to maintain data mappings in files and manage the files in dbt.

The following is an example of how dbt manages common data mappings. In this example, a model applies one-to-one 
data mappings on a field. Instead of creating a macro for the one-to-one data mappings, dbt allows you to create a 
seed for the one-to-one data mappings in the form of a CSV file and then reference it later.

![image](https://gist.github.com/assets/47337188/9160ba96-75b6-4c35-8e2b-5c75dccef875)



## References

ChatGPT 4

https://aws.amazon.com/blogs/big-data/manage-data-transformations-with-dbt-in-amazon-redshift/
