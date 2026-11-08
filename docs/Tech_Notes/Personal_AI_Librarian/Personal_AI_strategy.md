---
title: Personal Ai Strategy
category: Tech_Notes
tags:
  - Tech_Notes
  - Personal_AI_Librarian
status: In progress
created: 2026-10-30
updated: 2026-11-02
---
Stage 1
	✓ MkDocs
	✓ GitHub Pages

Stage 2
	✓ Metadata_Classifier.py
	 Note_Health_Report.py
	 Scheduled PowerShell

Stage 3: AI-Librarian
	AnythingLLM
	Ollama
	Knowledge Graph

Stage 4
	AI-generated metadata
	AI-generated summaries

---
Phase 1: Notes -> Obsidian -> Git -> GitHub -> MkDocs  -> Git;Hub Pages
Phase 2: AnythingLLM 
		(  Ollama -> AI platform
		+ Qwen2.5:7b -> Coding, Writing, AI-Librarian
		+ Llamma3:8b -> Writing
		+ Qwen3-vl:4b -> Vision process
		+ Gemma4:12b -> "on-demand analyst" ,AI-Librarian 
		+ nomic-embed-text -> Embedding
		+ LanceDB -> Vector Database
		+ )

Hardware: Laptop Lenovo 
	- Gen 11 i7-1185G7@3.00GHz
	- 8-Core (4-Physical, 4-Hyper Threads)
	- 16.0 GB RAM
	- Intel Iris Xe
	- 64-bit OS. Windows 11 Home

Software Applications:
- Obsidian Vault
	- metadata_classifier.py
	- MkDocs-Material (Zensical,  successor)
	- Note_health_report.py
	- Duplicate Detector
	- AI Tag Generator
	- AI Curator
- Git
- GitHub
	- GitHub Actions
	- GitHub Pages
- AnythingLLM
	- Ollama
	- nomic-embed-text
	- Llama3:8b
	- Qwen2.5:7b
	- Qwen3-vl:4b
	- Gemma4:12b
	- LanceDB


## Workflow (professional data pipelines)
Metadata_Classifier.py   --- Content Enrichment
        ↓
AI_Tag_Generator.py      --- Content Enrichment
        ↓
Duplicate_Detector.py    --- Content Analysis
        ↓
AI_Curator_Report.py      --- Content Analysis
        ↓
Note_Health_Report.py    --- Quality Validation
        ↓
Git Add / Commit / Pus    --- Publishing 
	↓
GitHub Pages / MkDocs    --- Publishing 


Mapping the tasks to specific tools while keeping **Ollama as the centralized model warehouse** is the exact right way to maximize your 16GB RAM.
However, you are missing **three critical connection pieces** that will bridge your applications (Obsidian, MS Word, and VS Code) directly to your local AI engine. Without these integrations, you will find yourself constantly copying and pasting back and forth, which ruins the workflow.

Here is what you need to add to complete your puzzle:

---
1. The Missing Piece for Creative Writing (MS Word Integration)

MS Word cannot natively talk to Ollama. To get Gemma 4 12B to write, brainstorm, or edit directly inside your documents, you need an add-in.

- **The Fix:** Install **OfficeAI** or use the open-source **Ollama-Word-Add-in**.
- **Alternative Route:** If you want a seamless local writing experience without configuring complex Word macros, consider drafting inside **Obsidian** or **LM Studio** first, then exporting to Word for final formatting.

2. The Missing Piece for Coding (VS Code Extension)

AnythingLLM is great for chatting about a project, but it doesn't give you inline code completion (like GitHub Copilot) while you type in VS Code.

- **The Fix:** Install the **Continue.dev** or **Twinny** extension in VS Code.
- **How it completes your stack:** You configure the extension to point directly to your background Ollama server. It will use **Qwen 2.5 7B** to give you lightning-fast, tab-to-complete inline code suggestions and highlighted code refactoring right inside your editor files [sports].

3. The Missing Piece for the AI-Librarian (Obsidian to AnythingLLM Bridge)

Your notes live in Obsidian, but your RAG database lives in AnythingLLM. You need a frictionless way to get your notes indexed by the librarian.

- **The Option A (Manual Sync):** Point AnythingLLM's document importer directly to your local **Obsidian Vault folder** on your hard drive. Whenever you update your notes, you just click "Resync" in AnythingLLM to update Gemma's memory.
- **The Option B (In-Editor AI):** If you prefer to stay entirely inside Obsidian, skip AnythingLLM for this specific task and install the **Smart Connections** or **BMO Chatbot** plugin inside Obsidian. These plugins allow Gemma 4 12B via Ollama to index your vault and chat with your notes without ever leaving Obsidian.

---

Optimized Workflow Blueprint

Once you add those integration layers, your final stack looks beautifully streamlined:

```
[ Your Core System Backend: Ollama ]
    │
    ├───► [Creative Writing] ──► MS Word + Word AI Plugin ──► Llama3.1:8b
    │
    ├───► [Coding Workflow]  ──► VS Code + Continue.dev  ──► Qwen2.5:7B
    │
	├───► [AI-Librarian]     ──► Obsidian Vault ──► AnythingLLM ──► Qwen2.5:7b
	│
	└───► [Embeddings]       --> AnythingLLM --> nomic-embed-text

[ Overall Resource Efficiency ]
🥇 Qwen2.5:7B
🥈 Llama3:8B
🥉 DeepSeek-R1
🏅 Gemma:12B (best reserved for occasional heavy analysis)

```

One Final Hardware Warning for Your i7 CPU

When using **VS Code with code-completion extensions**, the extension will constantly trigger small AI queries every time you press Enter or pause typing to predict your next line.

Because you are on a CPU-only setup, this can cause a slight typing lag if your CPU process priority isn't managed. Ensure your `run-ollama.bat` script (with the `BelowNormal` priority setting we discussed earlier) is running before you open VS Code!

---
batch run-ollama.bat

```
@echo off
title Ollama Background Optimizer
cls

echo =========================================================
echo  LAUNCHING OLLAMA WITH SYSTEM PRIORITY PROTECTION
echo =========================================================
echo.

:: 1. Launch the Ollama App at Below Normal Priority
echo [*] Starting Ollama background engine...
start "" /belownormal "%LOCALAPPDATA%\Programs\Ollama\ollama app.exe"

:: 2. Wait 5 seconds to ensure the local server port (11434) is fully awake
echo [*] Waiting for local server port to initialize...
timeout /t 5 /nobreak > nul

:: 3. Smart Unload: Tells Ollama to keep RAM empty (0s timeout) 
:: This registers the models with the system but forces RAM usage to 0 MB. 

echo [*] Optimizing memory footprint for llama 3.1 8B (for creative writing)...
curl -s -X POST http://localhost:11434/api/generate -d "{'model': 'llama3.1:8b', 'keep_alive': '15m'}" > nul

echo [*] Optimizing memory footprint for Gemma 4 12B...
curl -s -X POST http://localhost:11434/api/generate -d "{\"model\": \"gemma4:12b\", \"keep_alive\": 0}" > nul

echo [*] Optimizing memory footprint for Qwen 2.5 7B...
curl -s -X POST http://localhost:11434/api/generate -d "{\"model\": \"qwen2.5:7b\", \"keep_alive\": 0}" > nul

echo [*] Optimizing memory footprint for Qwen3 Vision 4B Instruct...
curl -s -X POST http://localhost:11434/api/generate -d "{\"model\": \"qwen3-vl:4b\", \"keep_alive\": 0}" > nul

echo [*] Optimizing memory footprint for nomic-embed-text...
curl -s -X POST http://localhost:11434/api/generate -d "{\"model\": \"nomic-embed-text\", \"keep_alive\": 0}" > nul

echo. 
echo ======================================================== echo SUCCESS: Your 16GB RAM is completely clean and protected! echo Ollama will load models dynamically on-demand when called. 

echo  SUCCESS: Your local AI environment is ready!
echo  You can now open VSCode, Word, Obsidian, or AnythingLLM.
echo ========================================================
echo.
timeout /t 3 > nul

```

----

