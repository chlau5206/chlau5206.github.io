---
title: Personal Ai Librarian Implement
category: Tech_Notes
tags:
  - Tech_Notes
  - Personal_AI_Librarian
status: In progress
created: 2026-10-29
updated: 2026-11-02
---

Phase 1: Set notes storing
Notes -> Obsidian -> git -> github -> github page
1. First trial: Obsidian + Jekyll
2. Second trial: Obsidian + MkDocs

Phase 2: Metadata standard
- create metadata for each .md files
- use folder structure and file info for details
- Build a Python [script](metadata_classifier.py.txt) to do it.
	- Features:
		✅ Recursive
		✅ Single-file mode
		✅ Dry-run
		✅ Only *.md
		✅ Skip index.md
		✅ Skip existing metadata
		✅ Generate metadata from path
		✅ Generate metadata from filename
		✅ Use filesystem dates
		✅ Re-runnable safely

Phase 3: Install Ollama
- [Ollama](irm https://ollama.com/install.ps1 | iex)
- 

Phase 4: Add AI-Model 
	[Your 16GB Lenovo Laptop]
	   ├── Workspace 1: Creative Writing ──> llama3.1:8b  (Better prose, handles long narratives)
	   ├── Workspace 2: Coding ────────────> Qwen 2.5 7B (Precise syntax, faster code blocks)
	   └── Workspace 3: AI-Librarian ──────> Gemma 4 12B (Stronger context retrieval & summarization)
	Embedding: --> nomic-embed-text
	Vector Store: -> LanceDB
	
	To verify Ollama running
		http://127.0.0.1:11434

Phase 5: run helpers
	- Metadata Auto Classifier --> done
	- Note Health Report 
	- AI Tag Generator
	- Duplicate Detector
	- AI Curator
