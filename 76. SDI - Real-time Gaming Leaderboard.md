# Real-time Gaming Leaderboard

## Problem and Scope
**Example questions to ask interviewer:**
- How is the score calculated?
- How to rank if two players have the same score?
- How many players are there? Do we only care about the top 10 users?
- Does the leaderboard reset on a schedule?
- Real-time?

**System requirements:**
- Scoring rule: 1 win = 1 point
- Players: ~5M daily active, ~25M monthly active.
- Resets every month
- Requirements:
  - Functional
    - Show top 10 players. 
    - Show a specific player’s rank. 
    - Bonus: show 4 players above & below.
  - Non-functional:
	- Must update in real-time (not batch).
	- Must be scalable, available, reliable.

**Estimation:**

We care about point scoring frequency and leaderboard reads, since they dominate traffic.
With 5M daily users, traffic averages about 50 users per second, but peaks can hit 250 users per second (peak factor 
×5). If each user plays 10 games a day, that’s about 500 QPS for scoring points, with peaks around 2,500 QPS.
Fetching the top 10 leaderboard happens once per user per day, so that’s only about 50 QPS.

## High-level Design

### API design
- POST /v1/scores (internal only): add points when a user wins.
  - user_id, points (usually 1)
  - Returns: 200 on success, 400 on failure
- GET /v1/scores: get top 10 players (score + rank + name).
- GET /v1/scores/{user_id}: get that user’s rank (and score).

### High-level architecture
There are two services:
- The game service allows users to play the game 
- The leaderboard service creates and displays a leaderboard

Request flow:
1. Client → Game Service: user wins; game service verifies it’s valid.
2. Game Service → Leaderboard Service: update score.
3. Leaderboard Service → Store: write the new score.
4. Client → Leaderboard Service: read top 10 or my rank.

Why game service, not let clients set scores?
- Clients set scores -> not secure (can spoof/change scores).
- Server must be authoritative.

Message queue between the game service and the leaderboard service?
- Not required for the core ask.
- Kafka only if scores must also feed analytics/notifications/other services.

### Data models

#### Relational Database


```
-- First time a user scores
INSERT INTO leaderboard (user_id, score) 
VALUES ('xinrong', 1);

-- Increment user’s score when they win again
UPDATE leaderboard 
SET score = score + 1 
WHERE user_id = 'xinrong';

-- Find a user’s rank
SELECT 
  RANK() OVER (ORDER BY score DESC) AS rank,
  user_id,
  score
FROM leaderboard;
```

This approach doesn’t scale, to get a user’s rank, we end up scanning/sorting the whole table.

#### Redis

```
# Add a new user with initial score = 0 (if not exists)
ZADD leaderboard_2025_09 0 "xinrong"

# Increment xinrong's score by 1 (e.g., win a match)
ZINCRBY leaderboard_2025_09 1 "xinrong"

# Get top 10 players (highest scores first, with scores included)
ZREVRANGE leaderboard_2025_09 0 9 WITHSCORES

# Get xinrong's current rank (0 = top rank, higher number = lower rank)
ZREVRANK leaderboard_2025_09 "xinrong"
```

Redis is in-memory (very fast) and has a perfect data type for this: **sorted sets**.

A **sorted set** is:
- Like a set, each member is unique (e.g., a user_id).
- Each member has a score (can repeat across users).
- Redis keeps members sorted by score automatically.
- Internally, it uses
  - a hash table (user → score)
  - a _skip list*_ (sorted users)
  - updates and lookups are O(log n)

A _skip list_ is a layered linked list with shortcuts. The bottom layer has all items in order, and 
upper layers contain fewer “promoted” items to skip over large sections. By moving right and down through layers, 
you can quickly find, insert, or delete items in O(log n) time.


**Reliability**:
- Use Redis persistence (RDB/AOF)
- Use a read replica; on failure, promote it and attach a new replica.
- Keep two SQL tables on the side:
  - Users (name, avatar, etc.).
  - Points log (user_id, score change, timestamp) — can rebuild Redis if needed.
- Small optimization: cache top-10 user profiles to avoid frequent DB lookups.

## Detailed Design

### Build options

- Run everything ourselves
  - Use Redis to keep the live leaderboard (a sorted set for each month).
  - Store player details (name, avatar, etc.) in MySQL.
  - When showing the leaderboard, fetch scores from Redis and details from MySQL.
  - For speed, we can cache the top 10 player details so we don’t keep hitting MySQL.
- Use the cloud (example: AWS)
  - API Gateway gives us the endpoints.
  - Lambda functions handle requests and talk to Redis + MySQL.
  - This way (serverless), we don’t manage servers, and the system scales automatically as player numbers grow.

### Scale Redis

Solution: split the data (sharding). Two ways:
- Fixed partition -> 
  - shard by score ranges (like 1–100, 101–200)
  - must move players when their scores cross a range
  - top 10 = only look at the highest range shard
  - rank = compute rank inside shard + add counts from shards above
- Hash Partition ->
  - Redis spreads data across many nodes automatically
  - easier writes
  - top 10 = fetch top players from every shard and merge them
  - rank = compute rank inside shard + fetch candidate ranks from all shards and globally merge/sort to find exact 
    position

### NoSQL alternative

Use a NoSQL store that:
- Handles high write throughput (score updates).
- Can read top-K quickly by sorting within a partition, fetching top-K from each partition and then get global top-K 
  (scatter-gather query pattern).

## References
ChatGPT

https://bytebytego.com/courses/system-design-interview/real-time-gaming-leaderboard
