---
title: Personal Ai Librarian Roadmap

category: Tech_Notes

tags:
  - Tech_Notes
  - Personal_AI_Librarian

status: completed

created: 2026-10-28
updated: 2026-11-02
---

### What an AI-Librarian Does
1. Find
2. Connect
3. Curate
4. Classify
5. Maintain

### Data Storage:
Obsidian -> Git->GitHub Pages

### Workflow order: 
- [X] Metadata auto classifier 
- [X] Markdown Cleanup
- [ ] Note Health Report
- [ ] Duplicate Detector
- [ ] AI Tag Generator 
- [ ] AI Curator Report

### 1. Metadata Auto Classifier

職責：
	- 修正 Frontmatter
	- 修正檔名
	- 補 Category
	- 補 Metadata
最先執行。

因為後面所有工具都要依賴：
YAML
	- title
	- category
	- tags

---
### 2. Markdown Cleanup

職責：
	- 修正 Markdown 格式
	- 修正 HTML Import
	- 修正 <br>
	- 移除奇怪格式

做完之後：
	Markdown = 乾淨版

---
### 3. Note Health Report
此時才做分析：
	- Missing Metadata
	- Empty Note
	- Large Note
	- Stale Note

結果才準確。

---
### 4. Duplicate Detector

我甚至會讓它分析：
``` Python
strip_front_matter(content)
```

之後再比較。

因為：
``` YAML
updated: 2026-11-04
```
	
不應該影響重複判定。

---
### 5. AI Tag Generator
此時：
	Metadata 已完成
	Markdown 已清理
	LLM 取得的是最佳內容。

---
### 6. AI Curator Report
最後執行。

因為它會依賴：
	- Category
	- Tags
	- Duplicates
	- Vault Health

全部結果。

它其實是：
	AI Librarian Weekly Summary

Phase 3.1 : Metadata Standards
---

title:

tags:

category:

status:

---
### Phase 3.2: Content Organization
folder:
docs/

    tech-notes/

    recipes/

    health/

    home/

subfolders:
recipes/

    italian/

    indonesia/

---
### Strategy for Your 3 Use Cases

Here is the ideal way to map your dual-model setup across your three intended workflows using AnythingLLM Workspaces:

```
[Your 16GB Lenovo Laptop]
   ├── Workspace 1: Creative Writing ──> Gemma 4 12B (Better prose, handles long narratives)
   ├── Workspace 2: Coding ────────────> Qwen 2.5 7B (Precise syntax, faster code blocks)
   └── Workspace 3: AI-Librarian ──────> Gemma 4 12B (Stronger context retrieval & summarization)
```

---
## AI Librarian Roadmap

### Phase 1 ✅

```text
Notes
 → Obsidian
 → MkDocs
 → Git
 → GitHub
```

### Phase 2 ✅

```text
Obsidian
 → MkDocs
 → AnythingLLM
```

### Phase 3 ✅

```text
AnythingLLM
 + Ollama
 + Qwen2.5:7B
 + Llama3:8B
 + Gemma 12B
 + nomic-embed-text
 + LanceDB
```

### Phase 4 🚧

```text
AI Librarian
```

Planned capabilities:

- Metadata generation
- Note health reports
- Duplicate detection
- Note classification
- Related note discovery
- Semantic knowledge search
- Knowledge curation