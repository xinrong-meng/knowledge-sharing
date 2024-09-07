# A Framework For System Design Interviews

The main goal is to see how you approach the problem, ask smart questions, and make good decisions. The interviewer 
cares more about your thought process than the final design. They want to see how well you can handle pressure, deal 
with unclear questions, and avoid mistakes like over-complicating things.

In short, focus on showing how you think through problems, work with the interviewer, and explain your choices 
clearly, rather than worrying about coming up with the “right” answer.

## A 4-step process

### Step 1 - Understand the problem and define the design scope

Here are the key actions:

1. Clarify the requirements: Ask questions to get clear on what features the system needs. For example:
   - Is this a mobile or web application?
   - What is the expected user base or scale?
   - What features are critical for the system?
2. Make assumptions if needed: If something isn’t clear or isn’t defined, make reasonable assumptions and write them 
   down. These will guide your design and prevent confusion later.
3. Identify key details: Focus on the scale of the system, the features, and technical constraints, such as the 
   technology stack or existing services the company uses.

**Example**

If you are asked to design a news feed system, you would ask about:
- The platform (web, mobile, or both)
- Key features like posting and viewing feeds
- Sorting methods (chronological or based on importance)
- User limits (e.g., how many friends can a user have?)
- Supported media types (images, videos, or just text)

### Step 2 - Propose high-level design and get buy-in

Now that you’ve clarified the problem, it’s time to sketch out a high-level design and get the interviewer’s 
feedback. This phase is more about collaborating than presenting a perfect solution.

1. Create a basic design blueprint: Use simple diagrams to show how the system will work. Include the key components 
like clients (web or mobile), APIs, databases, cache, content delivery networks (CDNs), and other infrastructure parts.
2. Collaborate with the interviewer: Treat the interviewer as a teammate. Ask for feedback and involve them in shaping 
   the design. This shows you’re open to collaboration and can adjust based on feedback.
3. Validate with quick calculations: If needed, perform quick estimates to ensure your design can handle the expected 
   scale. This helps to ensure your design will work for the system’s requirements.
4. Walk through use cases: Go over a few scenarios to test your design, which may help you discover any overlooked 
   details or edge cases.

### Step 3 - Design deep dive

Now, you’ll need to dive deeper into specific system components, prioritizing the most important parts based on feedback from the interviewer.

1. Prioritize key components: Work with the interviewer to identify which parts of the system to explore in detail. 
Depending on the interview focus, this might involve performance, scalability, or specific functionalities. 
2. Adjust focus based on feedback: Some interviews may focus on high-level concepts, while others may want you to explore technical challenges like bottlenecks, scalability, or performance tuning. Stay flexible and adapt to what the interviewer hints at or explicitly asks for.
3. Manage time wisely: Avoid spending too much time on minor details that don’t highlight your abilities. Instead, 
   focus on the critical aspects of system design. For instance, if designing a chat system, focus on reducing latency or managing user status (online/offline) rather than diving into irrelevant specifics.


### Step 4 - Wrap up

In the final step, you will address any remaining questions or provide additional thoughts. Here’s how to handle it effectively:

1. Identify system bottlenecks and suggest improvements: Acknowledge that no design is perfect. Discuss potential 
areas for optimization, such as scalability, performance, or fault tolerance. This shows you’re critically evaluating your work and are open to improvements.
2. Summarize your design: Recap your design for the interviewer, especially if you’ve presented multiple options. This 
   helps refresh their memory and reinforces your approach.
3. Discuss error handling: Talk about how your system deals with failure scenarios like server crashes or network 
   issues. This shows that you’re thinking about real-world operational challenges.
4. Mention operational aspects: Explain how you’d monitor system performance, track errors, and manage system updates 
   or rollouts.
5. Address future scalability: If your design supports 1 million users, suggest how you would modify it to handle 10 
   million users, demonstrating foresight and an ability to scale.
6. Propose refinements: If you had more time, mention any refinements or additional features you’d want to implement. 
   This shows that you’re continuously thinking about improving the design.


## Dos and Don’ts
Dos:
- Ask for clarification and don’t make assumptions.
- Understand the problem requirements and communicate your thought process.
- Offer multiple solutions when possible and focus on the critical components.
- Collaborate with the interviewer, treating them as a teammate.

Don’ts:
- Don’t dive into a solution before clarifying the problem.
- Avoid going too deep into a single component early on.
- Don’t think silently—communicate frequently with your interviewer.
- Don’t assume the interview is over until the interviewer says so.

## Time Allocation Guide

![image](https://github.com/user-attachments/assets/e05752e8-1b33-4dac-b324-90a0c7734715)


## References

https://bytebytego.com/courses/system-design-interview/a-framework-for-system-design-interviews

ChatGPT 4o