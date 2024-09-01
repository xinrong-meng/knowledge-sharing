# Back-of-the-envelope Estimation

The term comes from the idea that you could perform these calculations on the back of an envelope or any scrap of 
paper, implying that the calculations are informal and fast.

## Scalability basics

### Power of two

When using powers of 2 to measure data volume, the units are often referred to as binary prefixes.

- Byte (B): The basic unit of data, equivalent to 8 bits.
- Binary prefixes like KiB, MiB, GiB are based on powers of 2 and are different from the decimal-based prefixes like 
  KB, MB, GB (which are based on powers of 10 and often used in marketing for storage devices). For example, when 
  you say 1 GiB, you are referring to 1,073,741,824 bytes (2³⁰), while 1 GB (gigabyte) refers to 1,000,000,000 bytes 
  (10⁹).

### Latency

- Memory is fast but the disk is slow. 
- Avoid disk seeks if possible. 
- Simple compression algorithms are fast. 
- Compress data before sending it over the internet if possible. 
- Data centers are usually in different regions, and it takes time to send data between them.

### Availability numbers

High availability refers to a system’s ability to remain operational for an extended period, typically measured as a 
percentage of uptime. Most services fall between 99% and 100%.

Service level agreements (SLAs) define the expected uptime between a service provider and a customer, often set at 
99.9% or higher by major cloud providers.

#### Example 1: Estimate Twitter QPS and storage requirements

- Assumptions:
  - 300 million monthly active users.
  - 50% are daily active users (DAU).
  - Average of 2 tweets per day per user.
  - 10% of tweets contain media.
  - Data retention period: 5 years.

- QPS(Queries Per Second) Estimation:
  - Daily active users (DAU) = 300 million * 50% = 150 million.
  - Tweets QPS = 150 million * 2 tweets / 24 hour / 3600 seconds = ~3500.
  - Peek QPS = 2 * QPS = ~7000 (assuming the peak traffic is twice the average).

- Storage Estimation:
  - Tweet sizes: `tweet_id` = 64 bytes, `text` = 140 bytes, media = 1 MB.
    - tweet_id (64 bytes): Typically a unique identifier for each tweet, often stored as a 64-bit integer or a string.
    The 64-byte estimate may include overhead or metadata, though the actual size is usually smaller.
    - text (140 bytes): Represents the original 140-character limit for tweets. Each character is stored as 1 byte in
  UTF-8 encoding, so 140 characters require 140 bytes.
  - Daily media storage ≈ : 150 million * 2 * 10% * 1 MB = 30 TB per day
  - 5-year media storage ≈ 30 TB * 365 * 5 = ~55 PB.

#### Example 2: Estimate Instagram’s QPS and storage requirements

- Assumptions:
  - 1 billion monthly active users.
  - 60% are daily active users (DAU).
  - Average of 1.5 posts per day per user.
  - 100% of posts contain media (20% videos, 80% images)
  - Data retention period: 5 years.

- QPS(Queries Per Second) Estimation:
  - DAU: 600 million
  - Posts QPS:
    - Total Posts per Day = 600 million * 1.5 posts = 900 million posts
    - QPS = 900 million posts / (24 hours * 3600 seconds) ≈ 10400 QPS
  - Peak QPS:
    - Peak QPS = 2 * QPS = 20800 QPS (assuming the peak traffic is twice the average)

- Storage Estimation:
  - Media size: image size = 1 MB, video size = 10 MB
  - Daily media storage:
    - Image storage:
      - 80% of posts = 900 million * 80% = 720 million images
      - Total Image Storage = 720 million * 1 MB = 720 TB per day
    - Video storage:
      - 20% of posts = 900 million * 20% = 180 million videos
      - Total Video Storage = 180 million * 10 MB = 1800 TB per day
    - Total daily media storage:
      - Total = 720 TB (images) + 1800 TB (videos) = 2520 TB per day
  - 5-year media storage = 2520 TB/day * 365 days/year * 5 years ≈ 4600 PB (petabytes)

#### Example 3: Estimate Instagram’s Cache

- Assumptions:
  - 1 billion monthly active users.
  - 60% are daily active users (DAU).
  - Average of 1.5 posts per day per user.
  - Average post size: 1 MB
  - Only the most recent 10% of posts need to be cached for faster access.

- Cache Estimation:
  - Total posts per day = 600 million * 1.5 ≈ 900 million posts
  - Posts to be cached (10%) = 900 million * 10% = 90 million posts
  - Cache size = 90 million posts * 1 MB ≈ 90 TB

#### Example 4: Estimate Instagram's Number of Servers
- Assumptions:
  - Peak Concurrent Users: 50 million
  - Average _bandwidth_ required per user: 2 Mbps (for image-heavy content)
  
    _That's the average amount of data that each user is consuming in a second while using the platform. This data 
    includes the download of images, videos, and other media._
  - Each server can handle _10 Gbps_ of bandwidth.

    _Many modern servers are equipped with 10 Gbps network interface cards, which allow them to transmit and receive 
  data at speeds up to 10 Gbps._
  - Additional 20% buffer for load balancing and redundancy.

- Number of Servers Estimation:
  - Total bandwidth required = 50 million users * 2 Mbps = 100,000 Gbps
  - Number of servers = Total bandwidth / Bandwidth per server = 100,000 Gbps / 10 Gbps = 10,000 servers
  - With 20% buffer = 10,000 * 1.2 = 12,000 servers

## Tips

Back-of-the-envelope estimation is all about the process. Solving the problem is more important than obtaining 
results. Here are a few tips to follow:

- **Rounding and Approximation**: Focus on simplifying complex calculations during interviews. Precision isn’t expected; 
round numbers and approximate to save time. For example, instead of calculating “99987 / 9.1,” simplify it to “100,
000 / 10.”.

- **Write Down Your Assumptions**: Document assumptions for future reference, helping clarify your thought process.

- **Label Your Units**: Clearly indicate units to avoid confusion. For example, write “5 MB” instead of just “5” to ensure 
clarity.

## References

https://bytebytego.com/courses/system-design-interview/back-of-the-envelope-estimation

ChatGPT 4, specifically using examples created by the model.