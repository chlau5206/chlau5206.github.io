



Phase 1 - Collect and organize notes.
1. Obsidian

Phase 2 - Auto-tagging and categorization.
+ Obsidian
+ Ollama 
+ Llama 3
+ or use ChatGPT

Phase 3 - Semantic search and AI Wiki (add ChromaDB)
+ Obsidian
+ Ollama 
+ Llama
+ or use ChatGPT
+ ChromaDB

Phase 4 - Automatic ingestion of PDFs, YouTube videos, articles, etc.
+ Obsidian
+ Ollama 
+ Llama
+ or use ChatGPT
+ ChromaDB
+ n8n

Plan:
Notes -> Obsidian -> Embedding Model (nomic-embed) -> ChromaDB -> Ollama -> Llama 3 -> AI Assistant

Semi-Automatic Categorization
Category: Testing
Subcategory: Playwright
Tags:
 - browser
 - installation
 - troubleshooting

Stage 1: Knowledge Management
Focus on:

✅ Capture notes easily

✅ Auto-categorize notes

✅ Fast search

✅ Reduce duplicates

✅ Review and clean notes

Stage 2: AI Categorize
	Use: 
	- AI-Assisted Processing - Categorize notes
	- AI-generated tags
	- Duplicate Notes: Detect similar Notes

Stage 3: Search - Ask questions about your notes
Stage 4: Store - Obsidian, ChromaDB
Stage 5: Periodic cleanup


+ **Obsidian** - Stores knowledge
+ **n8n** - Content detects.  is an automation platform.  Automates everything.
+ **ChromaDB** - considered a NoSQL database, but it's more specifically a **vector database**.
+ **Qdrant** - a vector database, just like ChromaDB.
+ **Ollama** - not an AI model.  It's a **local AI model runner**.
+ **Llama 3** - the actual Large Language Model (LLM). Created by Meta.
+ **Embedding Model** - Converts text into vectors.  A numerical representation of meaning.  For example, 
	  Playwright browser crash  ->   [0.23, -0.11, 0.77, ...]
	  LLM -> creates -> Embeddings




Obsidian = Books on shelves
ChromaDB = Librarian who finds books
LLM = Researcher who reads books and answers questions


Obsidian -> local Ollama -> Vector Search -> Personal AI Wiki
Obsidian -> ChromaDB -> Qllama -> Llama 3
Obsidian -> ChromaDB -> Local AI Wiki -> Auto-Ingest YouTube/PDFs