**ChromaDB** is probably the easiest vector database to start with if your goal is an AI-powered Obsidian vault.

1. Obsidian = Stores notes
2. ChromaDB = Stores meanings of notes
3. LLM = Reads retrieved notes and answers questions

Architecture for an Obsidian AI Wiki
	Obsidian Vault
	       ↓
	Markdown Files
	       ↓
	Embedding Model
	       ↓
	ChromaDB
	       ↓
	LLM (ChatGPT/Claude/Ollama)
	       ↓
	Answer

Installation:
	pip install chromadb
Create a database:
{Python}
	import chromadb
	client = chromadb.PersistentClient("./mydb")
	collection = client.get_or_create_collection(
				    "obsidian"
				)
