# Data Models and Query Languages

Historically, data started out being represented as one big **tree** (the hierarchical model).

Some examples of hierarchical data models include:

- File systems: The file system on a computer is a hierarchical data model, where each file or folder is contained 
within a parent folder, forming a tree-like structure.

- Organizational charts: Organizational charts can be represented as hierarchical data models, where each employee is 
linked to a manager or supervisor, forming a hierarchy of reporting relationships.

- XML and JSON data: XML and JSON data formats are often organized hierarchically, with each element or object 
  containing nested sub-elements or objects.

But that wasn’t good for representing many-to-many relationships, so the **relational** model was invented to solve that problem. 

More recently, developers found that some applications don’t fit well in the relational model either. New **nonrelational** “NoSQL” 
datastores have diverged in two main directions:

- **Document** databases target use cases where data comes in **self-contained** documents and relationships between one 
document and another are rare.
- **Graph** databases go in the opposite direction, targeting use cases where anything is potentially **related** to everything.

One thing that document and graph databases have in common is that they typically don’t enforce a **schema** for the 
data they store, which can make it easier to adapt applications to changing requirements. However, your application 
most likely still assumes that data has a certain structure; it’s just a question of whether the schema is explicit 
(enforced on write) or implicit (assumed on read).  A more accurate term is **schema-on-read** (the structure of the 
data is implicit, and only interpreted when the data is read), in contrast with **schema-on-write** (the traditional 
approach of relational databases, where the schema is explicit and the database ensures all written data conforms to 
it).

## Document Data Models

Document databases reverted back to the hierarchical model in one aspect: storing nested records within their parent 
record rather than in a separate table.

However, when it comes to representing many-to-one and many-to-many relationships, relational and document databases 
are not fundamentally different: in both cases, the related item is referenced by a unique identifier, which is 
called a foreign key in the relational model and a document reference in the document model.

The document model has limitations: for example, you cannot refer directly to a nested item within a document, but 
instead you need to say something like “the second item in the list of positions for user 251” (much like an access 
path in the hierarchical model). However, as long as documents are not too deeply nested, that is not usually a problem.

The poor support for joins in document databases may or may not be a problem, depending on the application. For 
example, many-to-many relationships may never be needed in an analytics application that uses a document database to 
record which events occurred at which time.

A document is usually stored as a single continuous string, encoded as JSON, XML, or a binary variant thereof (such 
as MongoDB’s BSON). If your application often needs to access the entire document (for example, to render it on a 
web page), there is a performance advantage to this storage **locality**.

It’s worth pointing out that the idea of grouping related data together for locality is not limited to the document 
model. The column-family concept in the Bigtable data model (used in Cassandra and HBase) has a similar purpose of 
managing locality.

## Query Languages for Data

Each data model comes with its own query language or framework.

When the relational model was introduced, it included a new way of querying data: SQL is a **declarative** query 
language, whereas IMS and CODASYL queried the database using **imperative** code.

Many commonly used programming languages are imperative. An imperative language tells the computer to perform 
certain operations in a certain order.

In a declarative query language, like SQL or relational algebra, you just specify the pattern of the data you 
want—what conditions the results must meet, and how you want the data to be transformed (e.g., sorted, grouped, and 
aggregated)—but not how to achieve that goal. It is up to the database system’s **query optimizer** to decide which 
indexes and which join methods to use, and in which order to execute various parts of the query.

**MapReduce** is neither a declarative query language nor a fully imperative query API, but somewhere in between: the 
logic of the query is expressed with snippets of code, which are called repeatedly by the processing framework.

MapReduce is a fairly low-level programming model for distributed execution on a cluster of machines. Higher-level 
query languages like SQL can be implemented as a pipeline of MapReduce operations, but there are 
also many distributed implementations of SQL that don’t use MapReduce. Note there is nothing in SQL that constrains 
it to running on a single machine, and MapReduce doesn’t have a monopoly on distributed query execution.

## Graph-Like Data Models

But what if **many-to-many** relationships are very common in your data? The relational model can handle simple cases of 
many-to-many relationships, but as the connections within your data become more **complex**, it becomes more natural to 
start modeling your data as a **graph**.

A graph consists of two kinds of objects: vertices (also known as **nodes** or entities) and **edges** (also known as 
relationships or arcs). Many kinds of data can be modeled as a graph. Typical examples include:

- Social networks: Graphs are commonly used to represent social networks such as Facebook, Twitter, and LinkedIn. In 
these networks, nodes represent users, and edges represent their relationships, such as friend requests, followers, and connections.

- Transportation networks: Graphs are useful for representing transportation networks such as roads, railways, and 
air routes. In these networks, nodes represent locations, and edges represent the routes between them.

- Recommendation systems: Graphs are used to build recommendation systems that suggest products or services based on 
the user's behavior or preferences. In these networks, nodes represent products, and edges represent the relationships between them based on user behavior such as purchases or views.

- Fraud detection: Graphs can be used to detect fraud by modeling the relationships between different entities, such 
as bank accounts, transactions, and IP addresses. Suspicious patterns can be detected by analyzing the graph structure and identifying anomalous nodes and edges.

However, graphs are not limited to such homogeneous data: an equally powerful use of graphs is to provide a 
consistent way of storing completely **different types** of objects in a single datastore. For example, Facebook 
maintains a single graph with many different types of vertices and edges: vertices represent people, locations, 
events, checkins, and comments made by users; edges indicate which people are friends with each other, which checkin 
happened in which location, who commented on which post, who attended which event, and so on.

An example of graph-structured data:

![image](https://user-images.githubusercontent.com/47337188/232368392-4c4f9f26-7647-4fba-97b0-dc69f7d03a80.png)

There are several query languages that can be used with graph data models, each with their own syntax and features. 
Some of the most commonly used graph query languages include: Cypher and GraphQL.

## References

Designing Data-Intensive Applications By Martin Kleppmann

ChatGPT

## Related

[09. Database Overview](09.%20Database%20Overview.pdf)

[16. Wide-column Stores](16.%20Wide-column%20Stores.pdf)
