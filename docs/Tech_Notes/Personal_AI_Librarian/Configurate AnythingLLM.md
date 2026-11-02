To connect your local **Ollama** engine running **Gemma 4 12B** to **AnythingLLM**, you will configure two main sections within the settings menu: ==the **LLM Provider** (the model that talks to you) and the **Embedding Provider** (the model that processes your files)==.

Here is the exact step-by-step configuration layout to match your memory-safe 16GB RAM laptop setup:

---

Step 1: LLM Configuration (The Chat Engine)

Navigate to **Settings** (the gear icon on the bottom left) > **LLM Provider**, select **Ollama**, and input the following details:

- **Ollama Base URL:** `http://localhost:11434`
- **Model:** Select `gemma4:12b` from the dropdown list. _(If it doesn't appear, ensure your batch script is running and click the refresh icon)._
- **Token Context Window:** `8192` _(Though Gemma 4 supports much higher windows, limiting this to 8K or 16K ensures your 16GB CPU-only system doesn't run out of memory during very long conversations)._

---

Step 2: Embedding Configuration (The Document Parser)

Navigate to **Settings** > **Embedding Provider**. Since you are on a 16GB CPU-only machine, using a heavy local model for embedding can lag your system. **Do not use Gemma 4 for embeddings.** Use a specialized, lightweight embedding model instead.

Select **Ollama** and input these details:

- **Ollama Base URL:** `http://localhost:11434`
- **Embedding Model:** `nomic-embed-text` _(Open your Windows terminal and run `ollama pull nomic-embed-text` if you don't have it. It takes up less than 300MB of RAM and runs lighting-fast on your CPU)._
- **Max Embedding Chunk Length:** `512`

---

Step 3: Vector Database (The Librarian Memory)

Navigate to **Settings** > **Vector Database**.

- **Vector Database Provider:** Select **System Architecture (Default)**.
- _This locks in the built-in, disk-saving LanceDB instance we discussed, ensuring zero extra RAM overhead._

---

Step 4: Workspace Adjustments (Fine-Tuning)

Once your system-wide settings are saved, go back to your main dashboard and click **New Workspace** (e.g., name it "AI-Librarian"). Click the **Workspace Settings** gear next to its name to apply these crucial tweaks:

- **Chat Temperature:** `0.2` _(For the Librarian setup, keeping this low prevents the model from hallucinating or making up facts not found in your notes/manuals)._
- **LLM Thinking Mode:** **Disabled (Toggle Off)**. _(Turning off the deep chain-of-thought "thinking" mode gives your i7 CPU pure text speed. If you have a highly complex logic problem, you can toggle it back on temporarily)._

---

To link your local **Obsidian Vault folder** directly into your AnythingLLM workspace, you will ==use AnythingLLM's local folder connector==. This allows the application to read your markdown `.md` files straight from your computer's hard drive.

Here is the exact step-by-step process to link them:

---

Step 1: Open the Document Manager

1. Open **AnythingLLM** and click on your **AI-Librarian** workspace in the left sidebar.
2. Click on the **Upload / Manage Documents** icon (it looks like a folder with an arrow or a cloud icon) located right below the workspace name or near the top of the chat area.

Step 2: Use the Local Folder Importer

1. Inside the document manager window, look at the left-hand column under the upload zones.
2. Click on **Import Local Folder** or click the **Folder icon** option.
3. A file browser window will pop up. Navigate to where your local **Obsidian Vault** is saved on your hard drive (e.g., `C:\Users\YOUR_USERNAME\Documents\MyObsidianVault`).
4. Select the root folder of your vault and click **Select Folder** / **Open**.

Step 3: Pin or Move Your Notes to the Workspace

1. Once imported, you will see your entire Obsidian folder structure appear in the left-hand file tree of the AnythingLLM document manager.
2. Check the box next to your main Obsidian folder (or check individual sub-folders like "Notes" or "Manuals").
3. Click the **Move to Workspace** button in the middle of the screen. This stages your markdown files, preparing them to be read by your local database.

Step 4: Run the Embed Pipeline

1. Click the green **Save and Embed** button at the bottom right of the window.
2. **What happens now:** AnythingLLM will read your Obsidian markdown files, use your `nomic-embed-text` model via Ollama to turn the text into vector math, and store those math coordinates cleanly inside the built-in **LanceDB**.

---

Crucial Tip for 16GB Memory & CPU Stability

Because you are using an 11th Gen Intel CPU without a dedicated GPU, processing hundreds of notes all at once can max out your machine temporarily.

To prevent your laptop from choking during the initial embedding process:

- **Turn on your `run-ollama.bat` script first:** This ensures that the embedding process runs at `BelowNormal` priority. If you need to check an email or use your browser while AnythingLLM is indexing your vault, your laptop will stay completely smooth and responsive.
- **Do a bulk upload once, then sync:** If you add new notes to Obsidian later, simply open this document manager window again and click the **Resync / Sync** button next to your folder. AnythingLLM will smartly scan for _only_ the new or modified files rather than re-processing your entire vault from scratch.

----
For 16GB RAM
#### Key Variables to Set in System Variables:

- `OLLAMA_MAX_LOADED_MODELS` = `2` _(Allows 1 LLM + 1 Embedding model simultaneously without thrashing memory)_
    
- `OLLAMA_NUM_PARALLEL` = `1` _(Prevents memory usage from doubling per process)_
    
- `OLLAMA_KV_CACHE_TYPE` = `q8_0` _(Cuts memory usage for context windows roughly in half)_
    

> **How to set System Variables in Windows:**
> 
> Press **`Win + R`** $\$rightarrow type `sysdm.cpl` $\$rightarrow open **Advanced** tab $\rightarrow$ click **Environment Variables** $\rightarrow$ add/edit under the **System variables** panel (bottom section).

### 2. Fine-Tuning AnythingLLM Memory Settings (For 16GB RAM)

In AnythingLLM, "memory" refers to both **Vector Database Retrieval (RAG)** and **Chat History retention**. On a 16GB System running local LLMs, fine-tuning these settings stops the application from overwhelming your available system RAM or overflowing your model's context window.

#### A. Chat History Depth (Conversation Memory)

- **Location:** Workspace Settings $\rightarrow$ Chat Settings $\rightarrow$ **Chat History**
    
- **Recommended Setting:** **4 to 6 turns**
    
- **Why:** AnythingLLM re-sends previous messages back to Ollama on every new request to give the model memory. If set to 15–20 turns, long troubleshooting threads will send thousands of extra tokens per prompt, causing high memory usage and latency. Setting it between 4 and 6 retains essential conversation flow without wasting memory.
    

#### B. Document Chunk Size & Overlap (Text Splitter)

- **Location:** Settings (Gear icon) $\rightarrow$ AI Providers $\rightarrow$ **Text Splitter & Chunking**
    
- **Recommended Settings:**
    
    - **Text Chunk Size:** `1000` characters (~250 tokens)
        
    - **Text Chunk Overlap:** `50` to `100` characters
        
- **Why:** `nomic-embed-text` handles chunks around 1,000 characters cleanly. Overly large chunks force higher RAM usage during vector search, while overly small chunks fragment document context.
    

#### C. Vector Database Retrieval Density (RAG Snippets)

- **Location:** Workspace Settings $\rightarrow$ Vector Database Settings $\rightarrow$ **Max Context Snippets**
    
- **Recommended Setting:** **4 to 5 snippets**
    
- **Why:** Controls how many relevant document paragraphs AnythingLLM injects into your prompt when searching attached files. 4 to 5 snippets provide strong document grounding without overwhelming your model context.
    

### 3. Reviewing Your Startup Batch Script

Your updated batch script is clean and properly formatted! Commenting out `nomic-embed-text` from the `keep_alive: 0` flush step ensures it stays warm in RAM alongside your active chat model when setting `OLLAMA_MAX_LOADED_MODELS=2`.

#### Minor Fix for the `nomic-embed-text` Comment Line

In Windows `.bat` / `.cmd` scripts, lines beginning with `#` can throw a syntax error or output warnings because `#` is not a standard Windows batch comment operator (batch uses `::` or `rem`).