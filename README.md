# Charles Wiki

A personal knowledge base built with Obsidian, MkDocs, GitHub Pages, and local AI tools.

## Overview

Charles Wiki serves as a centralized repository for:

- Technical notes

- Home projects

- Recipes

The site is maintained in Markdown format and published automatically through GitHub Pages using MkDocs Material.

---

## Technology Stack

### Knowledge Management

- Obsidian

- Markdown

### Documentation Site

- MkDocs Material

- GitHub Pages

- GitHub Actions

### AI Librarian

- AnythingLLM

- Ollama

- Qwen2.5:7B

- Llama3:8B

- Gemma 12B

- nomic-embed-text

- LanceDB

---

## Repository Structure

```text

docs/

│

├── index.md

│

├── tech-notes/

│

├── recipes/

│   ├── indonesia/

│   └── italian/

│

├── health/

│

└── home/

```

---

## Local Development

Install dependencies:

```powershell

pip install -r requirements.txt

```

Start a local preview server:

```powershell

mkdocs serve

```

Open:

```text

http://127.0.0.1:8000

```

---

## Build Site

Build the static website:

```powershell

mkdocs build

```

Output:

```text

site/

```

---

## Publish Workflow

```text

Obsidian

    ↓

Markdown Notes

    ↓

Git

    ↓

GitHub

    ↓

GitHub Actions

    ↓

MkDocs Material

    ↓

GitHub Pages

```

---

## Metadata Auto Classifier

The repository includes a metadata generation utility:

```text

scripts/metadata_classifier.py

```

Features:

- Auto-generate front matter

- Category detection

- Tag generation

- Created / Updated timestamps

- Safe re-runnable operation

Preview changes:

```powershell

python metadata_classifier.py `

    --docs docs `

    --dry-run

```

Process the entire vault:

```powershell

python metadata_classifier.py `

    --docs docs

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

---

## License

Personal knowledge base and documentation repository.

Unless otherwise noted, content is maintained for personal reference and educational use.