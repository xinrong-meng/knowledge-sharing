# News Feed System

## What is a News Feed System

> Instagram Feed is a place where you can share and connect with the people and things you care about. When you open 
Instagram or refresh your feed, the photos and videos we think you care about most will appear towards the top of 
your feed. In addition to seeing content from people you follow, you may also see suggested accounts that are 
relevant to your interests.
> 
> — *Instagram Help Center*

A news feed system is the feature in apps like Instagram, LinkedIn, that shows you a scrolling 
list of updates from people you follow or recommended accounts.
- It takes content created by users (posts).
- Stores it in backend systems (databases, caches).
- When you open the app, it quickly generates a personalized feed by selecting, ranking, and displaying posts in 
  order (newest or most relevant).

## Problem and Scope

You should ask clarifying questions, for example:
- Is it mobile, web, or both?
- What features should we support? (posting, viewing friends’ posts, etc.)
- How is the feed sorted? (reverse chronological, score-based ranking, etc.)
- How many friends can a user have? (e.g. 5,000)
- What’s the traffic volume? (e.g. 10M daily active users)
- What content types? (text, images, videos) ￼

## High-level Design

### Feed publishing
1. User (browser/mobile) calls /v1/me/feed?content=Hello&auth_token={token}
2. Load Balancer spreads the request across Web Servers
3. Web Server validates the auth token and routes to internal services
4. Post Service saves the post (“Hello”) to the database and cache.
5. Fanout Service takes that post ID and pushes it into each friend’s feed (stored in cache for fast reads)
6. Notification Service alerts friends (push notifications / badges) that there’s new content
7. When friends open the app, their Feed API reads the feed cache and returns items quickly

### Newsfeed retrieval
1. User calls /v1/me/feed.
2. Load Balancer sends the request to one of the Web Servers.
3. Web Server (auth + routing) forwards to the Newsfeed Service.
4. Newsfeed Service looks up the user’s feed in the Newsfeed Cache (a per-user list of post IDs).
5. It then fetches the needed post details (text/media/author) from the content store/cache and returns the page.

## Detailed Design

### Feed publishing
#### Web servers
- Do auth + rate limiting at the edge.
- After, they route the request to the right internal service.

#### Fanout service (deliver posts to friends)
- Fanout on write (push)
  - When someone posts, we immediately write that post’s ID into each friend’s feed cache.
  - Pros: Feeds feel real-time; reads are fast (already precomputed).
  - Cons: If the author has millions of followers (hot key), pushing to all is slow/expensive. Also wastes work for 
    inactive users.

- Fanout on read (pull)
  - We don’t precompute. When a user opens the app, we pull recent posts from people they follow and build the feed on 
  demand.
  - Pros: No wasted work for inactive users; avoids the hot-key blast.
  - Cons: Reads are slower (work happens at read time).

- Hybrid (recommended)
  - Push for normal users (fast reads).
  -	Pull for celebrities / very high-fan accounts (avoid overload).
  -	Use consistent hashing to spread hot keys across many workers/caches.

**How the fanout pipeline works**
  1. Get friend IDs from the graph DB (friend/follow relationships).
  2. Get friend settings from user cache/DB (mute, privacy filters) and filter who should receive the post.
  3. Publish (friend list + new post_id) to a message queue.
  4. Fanout workers read the queue and append entries into the newsfeed cache

### Newsfeed retrieval
1.	Client → asks /v1/me/feed. 
2. Load balancer → sends the request to a web server.
3.	Web server → forwards it to the newsfeed service.
4.	Newsfeed service → looks up the user’s feed cache and gets a list of post IDs (e.g. [post123, post456, post789]).
5.	Gets user info (username, profile picture) from the user cache; Gets post content/media (text, images, videos) 
      from the post cache (media files themselves come from CDN).
6.	The service builds the hydrated feed (a JSON list with all details) and returns it to the client.

### Cache architecture
1. News Feed cache → list of post IDs for each user’s feed.
2. Content cache → post details (text, metadata); hot posts kept in extra-fast cache.
3. Social Graph cache → who follows who (followers/following lists).
4. Action cache → whether you liked, replied, or acted on a post.
5. Counter cache → numbers like likes, replies, followers, following.

## References
ChatGPT

https://bytebytego.com/courses/system-design-interview/design-a-news-feed-system

https://help.instagram.com/1986234648360433

