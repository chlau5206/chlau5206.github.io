**future MkDocs migration plan**, here’s a clean, practical, engineer‑friendly roadmap that ensures:

- your current wiki stays stable
- your folder structure remains MkDocs‑ready
- migration later is painless
- GitHub Actions is set up only when you need it
- you avoid the common pitfalls that make MkDocs migrations messy

This is the exact plan I’d give a senior engineer building a long‑term documentation system.

---

# ⭐ 1. Your Current Structure Is Already MkDocs‑Ready

You’ve done the most important part _without realizing it_:

```
docs/
  notes/
  recipes/
    french/
    japanese/
    thai/
  home/
  health/
```

MkDocs Material **loves** this structure.

You will NOT need to rename folders.  
You will NOT need to reorganize content.  
You will NOT need to rewrite links.

This is the biggest win.

---

# ⭐ 2. Keep Your Markdown Clean (No Jekyll‑specific syntax)

MkDocs supports:

- standard Markdown
- headings
- lists
- tables
- code blocks
- images
- links

But MkDocs does **not** support:

- Liquid templates (`{{ }}`)
- Jekyll includes
- Jekyll layouts
- Jekyll variables

So your migration plan is:

### ✔ Keep Markdown pure

### ✔ Avoid Liquid

### ✔ Avoid Jekyll‑specific features

You’re already doing this — good.

---

# ⭐ 3. Keep Front‑Matter Minimal

MkDocs ignores front‑matter, but it doesn’t break anything.

So keep your front‑matter simple:

---

title: Beef Bourguignon

nav_order: 1

---

MkDocs will ignore `nav_order`, but it won’t crash.

Later, MkDocs Material will auto‑generate navigation.

---

# ⭐ 4. When You’re Ready to Migrate: Add `mkdocs.yml`

Here’s the future file you’ll create:

site_name: Charles Wiki

theme:

  name: material

  features:

    - navigation.sections

    - navigation.expand

    - navigation.top

    - search.highlight

    - search.suggest

    - content.code.copy

    - content.tabs.link

    - content.tooltips

    - content.action.edit

    - content.action.view

nav:

  - Home: index.md

  - Documentation:

      - Notes: docs/notes/index.md

      - Recipes:

          - French: docs/recipes/french/index.md

          - Japanese: docs/recipes/japanese/index.md

          - Thai: docs/recipes/thai/index.md

      - Home: docs/home/index.md

      - Health: docs/health/index.md

### ✔ MkDocs will auto‑generate sidebar

### ✔ You can customize nav later

### ✔ Search becomes instant and fuzzy

### ✔ Dark mode is automatic

---

# ⭐ 5. Add GitHub Actions (CI/CD) Only When You Switch

MkDocs cannot be built by GitHub Pages directly.

So you’ll add **one** workflow file:

```
.github/workflows/deploy.yml
```

It will:

- install Python
- install MkDocs
- install Material theme
- build your site
- deploy to `gh-pages`

This is the only CI/CD you need.

You don’t need Docker, Jenkins, Azure DevOps, or anything else.

---

# ⭐ 6. Your Migration Steps (The Exact Checklist)

### ✔ Step 1 — Keep writing in Jekyll

No rush.

### ✔ Step 2 — When your wiki grows (50–100+ pages), create `mkdocs.yml`

### ✔ Step 3 — Add GitHub Actions workflow

### ✔ Step 4 — Build MkDocs locally once to confirm

### ✔ Step 5 — Switch GitHub Pages to `gh-pages` branch

### ✔ Step 6 — Remove Jekyll config (optional)

### ✔ Step 7 — Done

Your site becomes MkDocs Material.

---

# ⭐ 7. What You Gain After Migration

### MkDocs Material gives you:

- automatic sidebar
- automatic categories
- automatic ordering
- automatic breadcrumbs
- automatic next/previous links
- automatic search (instant, fuzzy, powerful)
- automatic dark/light mode
- automatic table of contents
- automatic code highlighting
- automatic collapsible sections
- automatic everything

You just write Markdown.

---

# ⭐ 8. What You Lose After Migration

### You lose:

- Jekyll front‑matter ordering
- Jekyll layouts
- Jekyll includes
- Jekyll Liquid syntax

But you don’t use any of those anyway.

So your migration is clean.

---

# ⭐ 9. When Should You Switch?

Here’s the honest recommendation:

### ✔ Stay with Jekyll + Just‑the‑Docs

until your wiki grows large enough that:

- navigation becomes annoying
- `nav_order` becomes tedious
- search feels slow
- you want a more modern UI
- you want automatic everything

### ✔ Switch to MkDocs Material

when your wiki becomes your long‑term knowledge base.

### ✔ Switch to Zensical

later (2027–2028) when it matures.

---

# ⭐ 10. Your Future MkDocs Migration Plan (Final Summary)

|Step|Action|
|---|---|
|1|Keep current Jekyll structure (already MkDocs‑ready)|
|2|Avoid Jekyll‑specific syntax|
|3|Add `mkdocs.yml` when ready|
|4|Add GitHub Actions workflow|
|5|Build MkDocs locally once|
|6|Switch GitHub Pages to `gh-pages`|
|7|Remove Jekyll config (optional)|
|8|Enjoy automatic navigation + search|

This is the cleanest, safest, most future‑proof path.

---

If you want, I can generate:

- your **future mkdocs.yml**
- your **GitHub Actions workflow**
- a **full MkDocs folder structure**
- a **migration checklist**
- a **side‑by‑side comparison of Jekyll vs MkDocs**

Just tell me what you want next.


-----------------------------------------------------------------
Good choice. Before we generate `mkdocs.yml`, I'd actually simplify your structure slightly for MkDocs.

## Recommended MkDocs Structure

Today (Jekyll):

chlau.github.io/
│
├── index.md
├── _config.yml
│
├── docs/
│   ├── index.md
│   ├── notes/
│   ├── recipes/
│   ├── home/
│   └── health/

Future MkDocs:

chlau.github.io/
│
├── mkdocs.yml
│
├── docs/
│   ├── index.md
│   ├── notes/
│   │   ├── index.md
│   │   ├── unicode.md
│   │   └── powershell.md
│   │
│   ├── recipes/
│   │   ├── index.md
│   │   ├── french/
│   │   ├── japanese/
│   │   └── thai/
│   │
│   ├── health/
│   └── home/

Notice:
- `docs/` becomes the site root
- Root `index.md` is no longer needed
- `_config.yml` is replaced by `mkdocs.yml`

---

# Minimal mkdocs.yml

If you want automatic navigation with minimal maintenance:

site_name: Charles Wiki
site_description: Personal Knowledge Base
theme:
  name: material
plugins:
  - search
markdown_extensions:
  - admonition
  - tables
  - toc:
      permalink: true

This works immediately but navigation order is alphabetical.

---

# Recommended Material Configuration

This is what I'd use for you:

site_name: Charles Wiki
site_description: Personal Knowledge Base
theme:
  name: material
  features:
    - navigation.sections
    - navigation.expand
    - navigation.top
    - search.highlight
    - search.suggest
    - content.code.copy

  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: blue
      accent: indigo
      toggle:
        icon: material/weather-night
        name: Dark mode

    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: blue
      accent: indigo
      toggle:
        icon: material/weather-sunny
        name: Light mode

plugins:
  - search

markdown_extensions:
  - admonition
  - tables
  - footnotes
  - toc:
      permalink: true



Features:
- Light/Dark mode switch
- Fast search
- Expandable sidebar
- Back-to-top button
- Code copy button
- Better table support

---

# Option 1: Fully Automatic Navigation

No `nav` section at all.

MkDocs automatically builds:

	Recipes
	    French
	    Japanese
	    Thai
	Notes
	    PowerShell
	    Unicode
	Home
	Health


Advantage:

- Add folders and md files
- Sidebar updates automatically
- Almost zero maintenance

This is my preferred method for your wiki.

---

# Option 2: Controlled Navigation

For larger sites:

	nav:
	  - Home: index.md
	  - Notes:
	      - Overview: notes/index.md
	      - Unicode: notes/unicode.md
	      - PowerShell: notes/powershell.md
	  - Recipes:
	      - Overview: recipes/index.md
	      - French:
	          - recipes/french/index.md
	      - Japanese:
	          - recipes/japanese/index.md
	      - Thai:
	          - recipes/thai/index.md
	  - Health: health/index.md
	

Advantage:

- Precise ordering

Disadvantage:

- Must update `mkdocs.yml` every time

---

# My Recommendation

Based on everything you've told me:

- Obsidian user
- Wants simple personal wiki
- Doesn't want navigation maintenance
- Wants search
- Hundreds of notes eventually

I'd use:

theme:
  name: material
plugins:
  - search

**No `nav:` section at all.**

Let MkDocs discover folders automatically.

That is actually the biggest advantage MkDocs has over your current Jekyll + Just-the-Docs setup. With Jekyll you're already fighting `nav_order`. With MkDocs you simply drop a new file:

docs/
└── recipes/
    └── korean/
        └── bibimbap.md

and it appears automatically in navigation and search.

For now, keep your Jekyll site working. As you add content, keep everything under `docs/` and avoid Jekyll-specific features. When you eventually switch, the migration will mostly be:

1. Delete `_config.yml`
2. Add `mkdocs.yml`
3. Add GitHub Actions workflow
4. Turn on Pages from `gh-pages`

and you're done.

----------------------------------
Absolutely. Since you're **not switching today**, I'd create the workflow file now and keep it in a separate folder or as a reference. When you're ready, just drop it into `.github/workflows/`.

For **MkDocs Material + GitHub Pages**, this is the workflow I'd recommend.

### `.github/workflows/mkdocs.yml`

name: Deploy MkDocs

on:
  push:
    branches:
      - main

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:

    runs-on: ubuntu-latest
    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install MkDocs
        run: |
          pip install mkdocs
          pip install mkdocs-material

      - name: Build Site
        run: |
          mkdocs build

      - name: Upload Site Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: site

  deploy:

    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    runs-on: ubuntu-latest
    needs: build

    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4

---

## Required GitHub Settings

When you eventually switch from Jekyll:

### Settings → Pages

Current:
	Deploy from a branch
	main /(root)

Change to:
	Source:
	GitHub Actions

Nothing else.

The workflow handles everything.

---

## Required Files

At migration time, your repo becomes:

chlau.github.io/
│
├── mkdocs.yml
│
├── docs/
│   ├── index.md
│   ├── notes/
│   ├── recipes/
│   ├── health/
│   └── home/
│
└── .github/
    └── workflows/
        └── mkdocs.yml

And you'll remove:
	[ _config.yml ]

because that's Jekyll-only.

---

## Local Preview

One huge advantage of MkDocs is testing locally before pushing.

Install:
	pip install mkdocs
	pip install mkdocs-material

Preview:
	mkdocs serve

Browse:
	 [http://127.0.0.1:8000]

Every saved Markdown file refreshes automatically.

This alone is one reason many people prefer MkDocs over Jekyll.

---

## My Recommendation

Keep your current setup:

Obsidian
    ↓
Git
    ↓
GitHub
    ↓
Jekyll + Just-the-Docs

until you've accumulated perhaps **30-50 notes** and have a feel for your organization.

Then create a branch such as:
	mkdocs-poc

and test:
	Jekyll vs MkDocs

side-by-side.

Because your content already lives under `docs/`, the migration effort will be surprisingly small. The biggest change will actually be deleting `nav_order` from your Markdown files and letting MkDocs generate navigation automatically.

-------------
## requirements.txt

Create:

Plain Text
	mkdocs==1.6.1
	mkdocs-material==9.6.22

Keep it in the repo root:

Plain Text
	chlau.github.io/
	│
	├── mkdocs.yml
	├── requirements.txt
	│
	├── docs/
	│ ├── index.md
	│ ├── notes/
	│ ├── recipes/
	│ ├── home/
	│ └── health/
	│
	└── .github/
	└── workflows/
	└── mkdocs.yml

---

## Update GitHub Actions

Replace:

YAML

- name: Install MkDocs
	run: |
		pip install mkdocs
		pip install mkdocs-material

with:
YAML
- name: Install dependencies
	run: |
	pip install -r requirements.txt

---

## Better Workflow (with Dependency Cache)

For faster builds:

YAML
	- name: Setup Python
	uses: actions/setup-python@v5
	with:
	python-version: "3.12"
	cache: "pip"
	- name: Install dependencies
	run: |
	pip install -r requirements.txt

---

## Optional Future Plugins

When your wiki grows, you may eventually want:

Plain Text

	mkdocs==1.6.1
	mkdocs-material==9.6.22
	mkdocs-awesome-pages-plugin==2.10.1
	mkdocs-git-revision-date-localized-plugin==1.4.7
	mkdocs-minify-plugin==0.8.0

These add:

- Automatic page ordering (`awesome-pages`)
- Last modified date on pages
- Smaller/faster generated site

I would **not install them yet**. Start simple.