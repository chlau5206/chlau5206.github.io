Based on the  goal of **collecting, organizing, finding, filtering, and consolidating notes**, I think **AnythingLLM** or an **Obsidian AI plugin** would get you 80-90% of the benefit. Building your own ChromaDB + Ollama + RAG stack is an interesting engineering project, but it may be solving a future problem you don't have yet. Your current pain point sounds more like knowledge organization than AI infrastructure.
If I were in your shoes, I'd spend my next weekend experimenting with **Smart Connections + Metadata Auto Classifier + Ollama**, not ChromaDB. That combination is much closer to "help me clean up the mess" than "build a futuristic AI knowledge system."

#**Mission:** 
Capture Notes -> AI Organizes -> AI Finds Duplicates -> AI Suggests Merges - Publish Best Knowledge

Phase 0 - Today's Archhitecture
	Notes -> Obsidian -> Git -> GitHub -> Jekyll / MkDocs

Phase 1 - Build Better Structure

Phase 2 - Add Metadate
	 ---
	category:
	tags:
	status:
	created:
	updated:
	---
Phase 3 = Build AI Classification
	New Note -> AI Suggests -> Approve
	Tools:
		Metadata Auto Classifier - Obsidian
		Auto Classifier - Obsidian
		Ollama (Local model)

Phase 4 - Related Note Discovery
	Tool:
		Smart Connections

Phase 5 - Weekly Cleanup

Phase 6 - Knowledge Consolidation

Phase 7 - Build Knowledge Maps

Phase 8 - Add Local AI Assistant
	Tools:
		Ollama
		Llama
Phase 9 - Add Semantic Search
	Tools:
		Chroma
			Smart connections
Phase 10 - Publication Pipeline
Final Architecture (2-3 Years)
          Notes

            ↓

         Obsidian

            ↓

      AI Librarian

            ↓

 ┌──────────┼──────────┐

 │          │          │

Category  Duplicate  Consolidation

Detection Detection     Review

 │          │          │

 └───────Knowledge─────┘

            ↓

       GitHub/MkDocs