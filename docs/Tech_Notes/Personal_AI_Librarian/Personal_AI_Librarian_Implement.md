---
title: Personal Ai Librarian Implement

category: Tech_Notes

tags:
  - Tech_Notes
  - Personal_AI_Librarian

status: completed

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

Phase 4: Add AI-Model 
	- add [Gemma 4 (12B)](https://ollama.com/library/gemma4:12b) <- good for laptop, unified.  
		  ollama run gemma4:12b
	- Optional Qwen3.8
