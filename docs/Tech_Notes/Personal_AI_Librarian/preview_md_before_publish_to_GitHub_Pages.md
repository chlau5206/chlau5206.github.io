---
title: Preview Md Before Publish To Github Pages
category: Tech_Notes
tags:
  - Tech_Notes
  - Personal_AI_Librarian
status: in progress
created: 2026-11-14
updated: 2026-11-20
---
## Workflow:
Obsidian -> Edit Markdown -> mkdocs serve -> Browser Preview 
	-> Git Commit -> Git Push 
## **MkDocs Local Server** 

1. Start MkDocs Local Server
PowerShell
> python -m mkdocs serve

2. browser 
   http://127.0.0.1:8000

------------------------------
## Option 2: Build Static Site Locally

Powershell
	mkdocs build