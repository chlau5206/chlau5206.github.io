site_name: Charles Notes
site_description: Personal Knowledge Base
site_author: Charles Loo

# Where your Markdown files live
docs_dir: docs

# Use the Material theme (best for wikis)
theme:
  name: material
  language: en
  features:
    - navigation.instant
    - navigation.sections
    - navigation.expand
    - navigation.tabs
    - search.highlight
    - search.suggest
    - content.code.copy

# Enable built-in search
plugins:
  - search

# Navigation structure (edit as needed)
nav:
  - Home: index.md
  - Recipes:
      - Beef Ribs: recipes/beef_ribs.md
      - Salmon: recipes/salmon.md
  - Tech:
      - PowerShell Unicode: tech/powershell_unicode.md
      - Python Notes: tech/python_notes.md
  - Home:
      - Water Heater: home/water_heater.md
  - Health:
      - Supplements: health/supplements.md
