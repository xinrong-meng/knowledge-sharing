# Rate Limiter

## What is a Rate Limiter

A rate limiter controls how many times a user or service can send requests in a certain time. If someone tries to 
send more than allowed, the extra requests will be blocked.

Let's distinguish between **resource limits** and **API rate limits** in real systems. For example, [here](https://docs.databricks.com/aws/en/resources/limits) documents both:

1. Resource limits
- Fixed caps on how much of a resource you can use.
- Examples: Max number of notebooks per workspace; Max number of jobs.
- These are *not rate limits*. They’re like *quota limits* (total allowed capacity), separate from traffic
  throttling.

2. API rate limits
- Throttling of API calls to prevent overload or abuse.
- Examples: `jobs/create`: max N requests per second.
- This matches what we are discussing here.

## Why Use a Rate Limiter?

- Prevent resource starvation caused by Denial of Service (DoS) attack
- Reduce cost: If you pay for each API call, rate limiting helps cut costs.
- Prevent servers from being overloaded.

## Problem and Scope
Example questions to ask interviewer:
- Is it a client-side or server-side?
- What should the rate limiter check: IP address, user ID, or something else? .
- How big is the system?
- Will the system work in a distributed environment?
- Is the rate limiter a separate service?

System requirements
- Accurately block extra requests
- Fast
- Use little memory
- Distributed
- Show clear errors (e.g. HTTP status code 429) when blocked
- Fault tolerance

## High-level Design

### Where to place the rate limiter?
- Client-side (unsafe, not recommended)
- Server-side
- Middleware, e.g. API Gateway (for SSL termination, auth, IP whitelist, static content)

|                            | Server-Side                                     | API Gateway                                                   |
|----------------------------------|---------------------------------------------------------------|---------------------------------------------------------------|
| **Tech stack fit**              | Must match your language and cache (e.g., Redis, Go, etc.)    | Works across languages and services                          |
| **Algorithm control**           | Full control; implement any algorithm                         | Limited to built-in algorithms supported by the gateway      |
| **Microservice integration**    | Manual setup inside your application                         | Easily added if gateway already handles auth/IP filtering    |
| **Engineering effort**          | High; requires time and skilled developers                    | Low; ready-made solutions available                          |
| **Flexibility**                 | Very flexible, fully customizable                             | Depends on vendor and config options                         |

### Algorithms for rate limiting

| Algorithm                  | How It Works                                                                                     | Pros                                              | Cons                                                                                      |
|----------------------------|--------------------------------------------------------------------------------------------------|---------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Token Bucket**           | Bucket with predefined capacity fills with tokens over time; each request uses one token.        | Allows bursts for short, simple, memory efficient | Hard to tune token rate and bucket size                                                   |
| **Leaking Bucket**         | Requests go into a queue, processed at a fixed rate; if the queue is full, requests are dropped. | Stable flow, memory efficient                     | Hard to tune outflow rate and bucket size; Bursts may block fresh requests if queue fills |
| **Fixed Window Counter**   | Count requests per fixed time window (e.g. 1 sec); block when predefined limit reached.          | Easy to implement, memory efficient               | Spikes at window edges may let too many requests through                                  |
| **Sliding Window Log**     | Track timestamps of each request in rolling window; block if over limit.                         | Very accurate                                     | High memory usage (stores rejected request timestamps)                                    |
| **Sliding Window Counter** | Blend of fixed and sliding; uses weighted average of past and current counts.                    | Handles burst traffic well, memory efficient      | Slightly less accurate; based on estimated count                                          |

The common idea of all 5 algorithms is: track how many requests happened in a time window, and block 
new ones if the limit is exceeded. They mainly differ in how they track requests and how flexible they are with 
bursts. See https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter for detailed explanations of 
algorithms.

### Architecture

All rate limiting algorithms need a counter to keep track of how many requests are sent from the same user, IP 
address, etc.

| Algorithm                 | What the "counter" refers to                             |
|---------------------------|----------------------------------------------------------|
| **Token Bucket**          | Number of **tokens in the bucket**                      |
| **Leaky Bucket**          | Number of **requests in the queue**                     |
| **Fixed Window Counter**  | A simple **count value per fixed time window**          |
| **Sliding Window Log**    | A **list (log) of timestamps** for recent requests      |
| **Sliding Window Counter**| Weighted sum of **counts from current and past window** |

Where do we store this counter?
- Not in a database -> too slow (disk access)
- Use in-memory cache -> fast and supports auto-expiry

## Detailed Design

### Rate limiting rules
- Rate limit rules (e.g. 5 logins per minute) are written in config files saved on disk
- Worker processes read these rules and store them in cache for fast access

### Exceeding the rate limit
- HTTP response code 429 (too many requests) to the client
- drop or enqueue the rate-limited requests to process later

### Distributed concerns

**Race Condition**
- Lock (too slow)
- Atomic operations

**Synchronization**
- Sticky sessions (always send the same client to the same limiter)-> Not scalable, hard to manage.
- Central data store like Redis (recommended)

## References
ChatGPT

https://bytebytego.com/courses/system-design-interview/design-a-rate-limiter

https://docs.databricks.com/aws/en/resources/limits

