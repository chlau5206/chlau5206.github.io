# Obsidian + AI: How to Build a Second Brain, an AI Database, or an LLM Wiki
Website: https://resource.lonelyoctopus.com/doc/ad5b2666-1a4c-4a5a-ae16-f34f622d42c8/
YouTube: https://youtu.be/4Hvkv_I8QDE

What Tina Huang is showing is usually a combination of:

1. **Obsidian** → stores your notes
2. **AI/LLM** → ChatGPT, Claude, Copilot, Gemini, etc.
3. **RAG (Retrieval Augmented Generation)** → AI searches your notes before answering
4. **Vector Database** → stores semantic embeddings of notes for AI search
5. **Automation** → AI automatically creates, updates, and links notes
## Why Obsidian works so well with AI
Obsidian is basically a single local folder, called a vault, full of markdown (.md) files. Open the folder in Obsidian and you get a clean interface for reading and writing notes, but under the hood it's still just plain text files sitting on your computer.

## Level 1: The AI Second Brain
This is the classic second brain concept (popularized by Tiago Forte), just upgraded. You still write the notes yourself. The difference is that instead of manually searching your own vault, an AI retrieves, analyzes, and interprets the information for you.
### How to build it

- **Step 1:** Create a folder and turn it into an Obsidian vault.
- **Step 2:** Add three .md files so the AI can navigate: ME.md (who you are, what you optimize for, how to talk to you), MAP.md (how your folders and notes are structured), and SKILLS.md (what you want the AI to be able to do).
- **Step 3:** Put your actual notes in a notes/ subfolder as .md files.
- **Step 4:** Put raw data (screenshots, stats, exports) in an evidence/ subfolder.
- **Step 5:** Connect an AI. General local agents like Claude Cowork, OpenClaw, or Hermes work well for conversational use. Coding agents like Claude Code, Codex, or OpenCode are better if you want to build something programmatically (dashboards, apps) from your notes. For full privacy, use an open-source agent harness with a local model.

## Level 2: The AI Database
This flips level 1 around: AI writes the notes into your vault, and you (or another AI) read them. This is the setup for people like me who don't want to write notes themselves but still want a rich, searchable record.
Multiple AI agents across multiple machines can all write to the same vault at once, since Obsidian Sync keeps everything updated and encrypted. My go-to models for this kind of writing are Gemini Flash and DeepSeek V3, or Qwen 3 32B running locally for full privacy.
### How to build it

- **Step 1:** Create a folder and Obsidian vault.
- **Step 2:** Point one or more AI agents at it with write access.
- **Step 3:** Let the AI file what it writes into .md files: research, meeting notes, saved articles, daily logs.
- **Step 4:** Browse, search, and link things by hand using Obsidian's search, graph view, and backlinks.
- **Step 5 (optional):** Connect another AI agent to retrieve, analyze, and interpret the data for you, the same way you would in a second brain.

## Level 3: The LLM Wiki

This is the full setup, a concept coined by Andrej Karpathy. You don't touch the vault at all. AI writes the notes, manages the whole thing, and retrieves and interprets it for you. As Karpathy puts it: Obsidian is the IDE, the AI is the programmer, and the vault is the codebase. You're just the observer.

### The three layers

Raw sources

Your curated, immutable collection of articles, papers, images, and data. The AI reads these but never modifies them. This is your source of truth.

Wiki

AI-generated markdown files: summaries, entity pages, comparisons, overviews. The AI owns this layer completely and updates it as new sources arrive.

Schema

A file like claude.md or agents.md that tells the AI how the wiki is structured and how to navigate the corpus.

### The three operations

- **Ingest:** drop a new source into raw sources and tell the AI to process it.
- **Query:** ask questions against the wiki; the AI searches, reads, and synthesizes an answer.
- **Lint:** the AI health-checks the wiki, resolving contradictions, flagging stale claims, and cleaning up orphaned pages.

Two special files help both you and the AI navigate as the wiki grows: **index.md** (a content-oriented catalog of every page, with summaries and metadata) and **log.md** (a chronological, append-only record of every ingest, query, and lint the AI has run).

### Who this is for

Karpathy describes several use cases: personal tracking (goals, health, self-improvement), deep research on a topic over weeks or months, reading a book and building out character or theme pages as you go, internal team wikis fed by Slack and meeting transcripts, and things like competitive analysis, trip planning, or hobby deep dives, basically anything where knowledge accumulates over time and you want it organized instead of scattered.

### How to build it

- **Step 1:** Create a folder and Obsidian vault.
- **Step 2:** Pick an AI and implement its LLM wiki skill. I used Hermes, which has this built in as a skill. Claude Code is the most documented option, with GitHub repos you can clone and run directly. Codex and OpenCode also work.
- **Step 3:** Try ingesting a few sources and let the AI take care of filing them.
- **Step 4:** Let it run autonomously over time, ingesting, querying, and linting on its own.


## Other Resources

[🔗AI second brain implementation→](https://youtu.be/rRa9td4oe7k?si=S24hZENPAertcg9a) [
🔗AI second brain example and commentary→](https://youtu.be/bdjYo-x4PUw?si=GZi9eQJ6Na52ctZ1) [
🔗Tina’s productivity system that uses AI database→](https://youtu.be/NMYQt25otes?si=ld8V4I8UhFQK9muF) [
🔗Andrej Kaparthy LLM wiki gist→](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) [
🔗Claude Code LLM Wiki→](https://github.com/nvk/llm-wiki) [
🔗LLM Wiki Hermes Skill→](https://hermes-agent.nousresearch.com/docs/user-guide/skills/bundled/research/research-llm-wiki)

Obsidian in 24 Minutes -- Tina Huang 
https://youtu.be/4Hvkv_I8QDE
Try out GenMail by Genspark for free 👉 [https://www.genspark.ai/genmail?utm_s...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYXFwNWd6Z19GMmh0VDhTdFIxc1F3cXxBSTVJdTVzbmhETFh0NW9qVXVwbmNJUVU5dWhMMXlZQmJFXzMxTkh3NDBTeDNMR2E3NzRrV2ZyQUUyb2RRcms3U28tWEJzMDY5aXJ2WmVDZGcwaTdaSFh1RlVXZ2ZKTmJ5dzVp&q=https%3A%2F%2Fwww.genspark.ai%2Fgenmail%3Futm_source%3Dyt%26utm_campaign%3Dtinahuang03&v=4Hvkv_I8QDE) In this video I go through Obsidian and its 3 levels of integration with AI. 📚 Get the complete resource document: [https://resource.lonelyoctopus.com/si...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYTdXdUFXWkk5QTdITTUzR044aVZOVHxBSTVJdTV1d2R3Z3k5aW5ZX0Y0bXFnMlFxOFhFckE1M2tiZ3V2WUFUOW4wQkxTaXYyb2NWTi1iY0poSGVJYk5VLVp2Q2ZHU3hSNklrODFuX282aWNCdFRrWWkzWGplSUxHQ1lS&q=https%3A%2F%2Fresource.lonelyoctopus.com%2Fsignup%2Fobsidian-in-24-minutes%2F&v=4Hvkv_I8QDE) 💜 Registration to Hermes Workshop now open!: [https://www.lonelyoctopus.com/hermes-...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYTNUNlE5QnB0dW5zWVFYZDBuQlNtb3xBSTVJdTV2cHFIUDhFbWNLTERUYWE0Q0lxMFoxVkdpb0VhUjNLWW0tSjVhQ1hhdDlETWFXVk1YRm1SUDhxS19HWXhqQ0FwMThGVWstcXRrNUFEVVdLTDNRbWNYa2VmSkJFX1VG&q=https%3A%2F%2Fwww.lonelyoctopus.com%2Fhermes-workshop-2026&v=4Hvkv_I8QDE) 🐙 Free 28-Day AI Sprint Roadmap - pick your goal to get a clear, day-by-day path forward 👉 [https://www.lonelyoctopus.com/ai-spri...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWW9TODdwU3dnRHQyOVpLekZsVTMzS3xBSTVJdTV0RzFXcFZZc1liaTg0VmFJcUVoSVZ6eTVwM0hVTy1iNmVBX3NKdl9UUlRlNmpKd0t5bDJRU3hwTW0xRXhJcVBUdU93SFpFRFQ1TV9BUDVTSUFHSUpjT0k2UDdrNXZF&q=https%3A%2F%2Fwww.lonelyoctopus.com%2Fai-sprint-roadmap&v=4Hvkv_I8QDE) 🤖 Want to get ahead in your career using AI? Join the waitlist for my AI Agent Bootcamp: [https://www.lonelyoctopus.com/ai-agen...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWW1xUkhsNW9MQ0FKaHkwZ0E5dXZMQ3xBSTVJdTVzTGRkbUZuSjVYTlZfMktzRmFpUmJLZmFEdDAzWnNPcU1fRE9nVGpsSERlUGVKbVVvM0xHZ2h3SDVQR0VHV21lZUx0SS04eXg5QXg0Z2M5Z3dfblVmTGxrRmpNcVpf&q=https%3A%2F%2Fwww.lonelyoctopus.com%2Fai-agent-bootcamp&v=4Hvkv_I8QDE) 🤝 Business Inquiries: [https://tally.so/r/mRDV99](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWjdJWEJUb0JZeTVyU3FvU19sMG8wa3xBSTVJdTV0cmNIU2ZCNER3RW82UThIUUhNZDQ5M19TQkl5REVvY0YxeWRQSjZ2UHUyeGVQLUZwOE1jeGJveXdfVDNtR2RNVDV1b1ZmWk02T0RSbjhhSmE2aUx1d3FCNzhBV3pi&q=https%3A%2F%2Ftally.so%2Fr%2FmRDV99&v=4Hvkv_I8QDE) 🖱️Links mentioned in video ======================== 🔗Affiliates ======================== My SQL for data science interviews course (10 full interviews): [https://365datascience.com/learn-sql-...](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWTFocEl1alJibVpOdk5hZFVxTEcwVXxBSTVJdTVzOVZ6WnVNVWhvMkUtQ3Rzbzl6RzBYZzJJWFZGLUVxM04wYkx1QWRnWTZ4ZVZWM1ZRbTZtTTV1dXZfVEtPTUZ4R2hwaFNkb0FmXzBnTEdySG5kWHh0Q1A1SkFPSDRD&q=https%3A%2F%2F365datascience.com%2Flearn-sql-for-data-science-interviews%2F&v=4Hvkv_I8QDE) 365 Data Science: [https://365datascience.pxf.io/WD0za3](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWmtnRi0wN1ZhTDd1WHRDaDNZeVg4UXxBSTVJdTV0NGI2QjctS1UySXlDTHk2dlZBOURwRElyZ1NQZmI1d1V6WjJhSi1ZajhVZEktc0szRHRKM0FiclJpdGpZNDVQdmdNZ0I3cU41ZzZYUWc0T2VEQlJzM0FMaXlGQ0ww&q=https%3A%2F%2F365datascience.pxf.io%2FWD0za3&v=4Hvkv_I8QDE) (link for 57% discount for their complete data science training) Check out StrataScratch for data science interview prep: [https://stratascratch.com/?via=tina](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYTBGTkE4Q1RaNEZvbUlaUDF6TkhQU3xBSTVJdTV2SkdLeXlBaFZPdWN4enNIODA5MnkxMXhlcmJ0MTRxa294eEVnYUFkLWVxNlNla0VnbXlOdHdKWmlvUEl4czVDa0JfUmdYM0NLMXZEdkpQeng4dkdqT0dQbkxWdThz&q=https%3A%2F%2Fstratascratch.com%2F%3Fvia%3Dtina&v=4Hvkv_I8QDE) 🎥 My filming setup ======================== 📷 camera: [https://amzn.to/3LHbi7N](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWjVWZEdLOEFpYnRWempDUVpQYzhqRnxBSTVJdTV2dFRvV19zbG5DWVpHVlc2SG9ZR3hEVE9uSjFfOHNCVG1WU1U0by0xUEV1aVEwOExvYnNJb2NQUTNabzE1TDZuRi1ScUM4TVktYkJ4Umt4cnp2UWcwTjhiZUVZRzVv&q=https%3A%2F%2Famzn.to%2F3LHbi7N&v=4Hvkv_I8QDE) 🎤 mic: [https://amzn.to/3LqoFJb](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWVdpbkRucjVOd3RvVzl1Y2MyR24yY3xBSTVJdTV0eXJHU2R0a3MwMFNCakZCanJZVlV1eFExdFo1b09FNDV4ZURkTHVULWlLbXoyVFVfcmo4WkRsTHE0MExHdmt0Wjd6aXFrNmEyZ2pvR2tzYmF6bG5uN1kzZHYwTnNH&q=https%3A%2F%2Famzn.to%2F3LqoFJb&v=4Hvkv_I8QDE) 🔭 tripod: [https://amzn.to/3DkjGHe](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYjJLQTlBcngxczNmaTRMdXZ1TF9JbnxBSTVJdTV0LWlqRXA3QzZ3S0hsZWFSM3YwaDMzUEExNDlWb3k1aUV2WEJMdHBrVmh3Y0pTMTFNeVplZzlxSXBLUm96b1JUWHhKVnRTZHpHbUtpMGRtTkdTenZNZG5qMXR6LVZO&q=https%3A%2F%2Famzn.to%2F3DkjGHe&v=4Hvkv_I8QDE) 💡 lights: [https://amzn.to/3LmOhqk](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYUJsTmhCRVBBZkNYVmU3c2g4Y0pOS3xBSTVJdTVzdXdtRzVsNnJvcG9kUE50NndLOUdnZWdKYnByaDlEdzhoM2lJNjFtTWJzalpmMGhfSzRVd20zcjVvejh6dDRCUnp1RmlreVBsOHkzVGtZUWZtRlU3QU8wdm9NNkZa&q=https%3A%2F%2Famzn.to%2F3LmOhqk&v=4Hvkv_I8QDE) ⏰Timestamps ======================== [00:00](https://www.youtube.com/watch?v=4Hvkv_I8QDE) Intro [01:19](https://www.youtube.com/watch?v=4Hvkv_I8QDE&t=79s) Obsidian Major Features [06:39](https://www.youtube.com/watch?v=4Hvkv_I8QDE&t=399s) AI Second Brain [12:22](https://www.youtube.com/watch?v=4Hvkv_I8QDE&t=742s) AI Database [16:30](https://www.youtube.com/watch?v=4Hvkv_I8QDE&t=990s&pp=0gcJCWMAwfN6Pr3D) LLM Wiki [24:15](https://www.youtube.com/watch?v=4Hvkv_I8QDE&t=1455s) Quiz 📲Socials ======================== instagram:   [![](https://www.gstatic.com/youtube/img/watch/social_media/instagram_1x.png) / hellotinah](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYW1Kd2x2TVlSZ21IZ3BEZ3lCWkt1NnxBSTVJdTV2eDZkazNWcVRTNHRKemNRNVhab1luUWk1UzYzUWgzdkNkaGRnQ2xqTXloY3pGUmxBWmR3Y2I3dmJ1NG5BWnpZZjdmTG1BYkdlN2NHX05fMGN1N0lfQUdxclBOdk1i&q=https%3A%2F%2Fwww.instagram.com%2Fhellotinah%2F&v=4Hvkv_I8QDE)   linkedin:   [![](https://www.gstatic.com/youtube/img/watch/social_media/linkedin_1x.png) / tinaw-h](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYkJrQ2xlM3RiVDBfOGF0cmtwWkNDM3xBSTVJdTVzQXVJYXl4Y0NNdEFRT3ZlXzIzWEJ0QnVOLWxNZUNHRlI1MTRsNEhOSE9CdEpPRnZSSEZ2cEdIRndONWZoLTdnZ29rbVRkTEZmTXZNRlBmOG56TU1ORllrdFoxNFcw&q=https%3A%2F%2Fwww.linkedin.com%2Fin%2Ftinaw-h%2F&v=4Hvkv_I8QDE)   tiktok:   [![](https://www.gstatic.com/youtube/img/watch/social_media/tiktok_1x.png) / hellotinahuang](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYmoxWmNoQ3ZzSV9sN1l5SXlHTl9mNHxBSTVJdTV0RXp1Rzhyc3A2N29XbFlKcFRIR3JLTHhOa0tGSElqQmRsVmd4Z21jOHB6cDNycWkyWElta0lLUEdDZkdDdFlsTDJMZzFGR1E2blM3RlRnTzhxelVDSjhsbTFfU2xC&q=https%3A%2F%2Fwww.tiktok.com%2F%40hellotinahuang&v=4Hvkv_I8QDE)   discord:   [![](https://www.gstatic.com/youtube/img/watch/social_media/discord_1x.png) / discord](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IWjBlT3ozbkZjdU5KVjYwRXVnTWVJcnxBSTVJdTV0VjFwbHVucVV2WHl6YVFvZEltTEp2dTdKenNoM0tUWmxZTVNIMi1VdXUwV1pPNy1KUnhkSWVRaVpfaXJfQTRTT2pXLXJUZ3ZEVU5CLU9sUDVTZ2t4MEZRcGtNRGNf&q=https%3A%2F%2Fdiscord.gg%2F5mMAtprshX&v=4Hvkv_I8QDE)   🎥Other videos you might be interested in ======================== How I consistently study with a full time job:    [![](https://www.gstatic.com/youtube/img/watch/yt_favicon_ringo2.png) • How I consistently study with a full time ...](https://www.youtube.com/watch?v=INymz5VwLmk)   How I would learn to code (if I could start over):    [![](https://www.gstatic.com/youtube/img/watch/yt_favicon_ringo2.png) • How I would learn to code (if I could star...](https://www.youtube.com/watch?v=MHPGeQD8TvI&t=84s)   🐈‍⬛🐈‍⬛About me ======================== Hi, my name is Tina and I'm an ex-Meta data scientist turned internet person! 📧Contact ======================== youtube: youtube comments are by far the best way to get a response from me! linkedin:   [![](https://www.gstatic.com/youtube/img/watch/social_media/linkedin_1x.png) / tinaw-h](https://www.youtube.com/redirect?event=video_description&redir_token=QUlxb01IYjgzN19FWmJsaldkZkllRTA2eHBmVXxBSTVJdTV2LVVSYm11aXZZMHl3YkZFcmwwQkVsZHZIc3dVamR3cnR2VWtHLU5rcU96WW53SXAwNlRkb3k5cUhqNm4ySF9xaTRJeWY4eGtncWxrNVJGTkt3cURza3ROeGJpQlBr&q=https%3A%2F%2Fwww.linkedin.com%2Fin%2Ftinaw-h%2F&v=4Hvkv_I8QDE)   email for business inquiries only: tina@smoothmedia.co