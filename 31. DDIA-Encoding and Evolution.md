# Serialization

Programs usually work with data in (at least) two different representations:

- In memory

  Data is kept in objects, structs, lists, arrays, hash tables, trees, and so on. These data structures are optimized for efficient access and manipulation by the CPU (typically using pointers).
- On disk / Over the network

  Data is encoded as some kind of self-contained sequence of bytes (for example, a JSON document). Since a pointer wouldn’t make sense to any other process, this sequence-of-bytes representation looks quite different from the data structures that are normally used in memory.

Thus, we need some kind of translation between the two representations. The translation from the in-memory representation to a byte sequence is called encoding (also known as serialization or marshalling), and the reverse is called decoding (parsing, deserialization, unmarshalling).

## 1. Language-Specific Formats

Many programming languages come with built-in support for encoding in-memory objects into byte sequences. For example, Java has java.io.Serializable, Python has pickle, and so on.

Pros:

- Convenient, because they allow in-memory objects to be saved and restored with minimal additional code.

Cons:

- Tied to a particular programming language, and reading the data in another language is very difficult.
- Security problems: In order to restore data in the same object types, the decoding process needs to be able to instantiate arbitrary classes. If an attacker can get your application to decode an arbitrary byte sequence, they can instantiate arbitrary classes, which in turn often allows them to do terrible things such as remotely executing arbitrary code.
- Forward and backward compatibility：Versioning data is often an afterthought in these libraries: as they are intended for quick and easy encoding of data.
- Efficiency (CPU time taken to encode or decode, and the size of the encoded structure) is also often an afterthought.

For these reasons it’s generally a bad idea to use your language’s built-in encoding for anything other than very 
transient purposes.

## 2. JSON, XML, and Binary Variants

Pros:

- Standardized encodings that can be written and read by many programming languages.
- Textual formats, and thus somewhat human-readable.

Cons:

- Ambiguity around the encoding of numbers.
- Missing support of binary strings (sequences of bytes without a character encoding).
- Optional complicated schema (XML, JSON) / No schema (CSV).

Despite these flaws, JSON, XML, and CSV are good enough for many purposes. It’s likely that they will remain popular,
especially as **data interchange formats** (i.e., for sending data from one organization to another). In these 
situations, as long as people agree on what the format is, it often doesn’t matter how pretty or efficient the 
format is. 

### Binary Encoding

JSON is less verbose than XML, but both still use a lot of space compared to binary formats.

This observation led to the development of a profusion of binary encodings for JSON (MessagePack, BSON, BJSON, UBJSON, BISON, and Smile, to name a few) and for XML (WBXML and Fast Infoset, for example). 

Some of these formats extend the set of datatypes, but otherwise they keep the JSON/XML data model unchanged.

In particular, since they don’t prescribe a schema, they need to include all the object field names within the encoded data.

## 3. Thrift and Protocol Buffers

### Schema
Both Thrift and Protocol Buffers require a schema for any data that is encoded.

Example schema:

<img width="654" alt="image" src="https://user-images.githubusercontent.com/47337188/184458163-5e4a4cf3-0533-43f0-9e0b-3995d19b98f5.png">

Thrift and Protocol Buffers each come with a **code generation tool** that takes a schema definition like the ones shown
here, and produces classes that implement the schema in various programming languages. Your application code
can call this generated code to encode or decode records of the schema.

### Encoding

- Example record encoded using Thrift’s CompactProtocol:

![image](https://user-images.githubusercontent.com/47337188/184458094-022bef43-cd8f-4cd7-96fb-a8f18db75b51.png)

It does this by packing the field type and tag number into a single byte, and by using variable-length integers. 
Rather than using a full eight bytes for the number 1337, it is encoded in two bytes, with the top bit of each byte 
used to indicate whether there are still more bytes to come. This means numbers between –64 and 63 are encoded in 
one byte, numbers between –8192 and 8191 are encoded in two bytes, etc. Bigger numbers use more bytes.

- Example record encoded using Protocol Buffers:

![image](https://user-images.githubusercontent.com/47337188/184458110-eb3b5161-cdae-4a29-8114-92bee89ccd3f.png)

It does the bit packing slightly differently, but is otherwise very similar to Thrift’s CompactProtocol.

The big difference between Thrift/Protocol Buffers and JSON/XML is that there are no field names (userName, 
favoriteNumber, interests). 
Instead, the encoded data contains field tags, which are numbers (1, 2, and 3). Those are the numbers that appear in 
the schema definition. Field tags are like aliases for fields—they are a compact way of saying what field we’re 
talking about, without having to spell out the field name.

### Schema Evolution

Schemas inevitably need to change over time. We call this schema evolution.

#### Field Tags

In Thrift and Protocol Buffers, an encoded record is just the concatenation of its encoded fields.

Each field is identified by its tag number and annotated with a datatype. If a field value is not set, it is simply 
omitted from the encoded record. From this you can see that field tags are critical to the meaning of the encoded data.

You can change the **name of a field** in the schema, since the encoded data never refers to field names, but you cannot change a field’s tag, since that would make all existing encoded data invalid.

You can add **new fields** to the schema, provided that you give each field a new tag number.
If old code tries to read data written by new code, including a new field with a tag number it doesn’t recognize, it can simply ignore that field.

The datatype annotation allows the parser to determine how many bytes it needs to skip. This maintains **forward compatibility**: old code can read records that were written by new code.

As for **backward compatibility**, As long as each field has a unique tag number, new code can always read old data, because the tag numbers still have the same meaning. The only detail is that if you add a new field, you cannot make it required. "required" enables a runtime check that fails if the field is not set.

Removing a field is just like adding a field, with backward and forward compatibility concerns reversed.

#### Datatypes

Changing the datatype of a field is possible. But there is a risk that values will lose precision or get truncated.

For example, say you change a 32-bit integer into a 64-bit integer. New code can easily read data written by old code, because the parser can fill in any missing bits with zeros. However, if old code reads data written by new code, the old code is still using a 32-bit variable to hold the value. If the decoded 64-bit value won’t fit in 32 bits, it will be truncated.

### Summary

Pros:
- They can be much more compact than the various “binary JSON” variants, since they can omit field names from the 
encoded data.
- The schema is a valuable form of documentation, and because the schema is required for decoding, you can be sure 
  that it is up to date (whereas manually maintained documentation may easily diverge from reality).
- Keeping a database of schemas allows you to check forward and backward compatibility of schema changes, before 
  anything is deployed.
- For users of statically typed programming languages, the ability to generate code from the schema is useful, since 
  it enables type checking at compile time.

Many data systems also implement some kind of proprietary binary encoding for their data. For example, most
relational databases have a network protocol over which you can send queries to the database and get back responses.
Those protocols are generally specific to a particular database, and the database vendor provides a driver (e.g.,
using the ODBC or JDBC APIs) that decodes responses from the database’s network protocol into in-memory data structures.


## References*

Designing Data-Intensive Applications By Martin Kleppmann







