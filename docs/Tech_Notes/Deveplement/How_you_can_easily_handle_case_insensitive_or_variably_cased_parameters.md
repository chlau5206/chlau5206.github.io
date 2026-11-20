---
title: How You Can Easily Handle Case Insensitive Or Variably Cased Parameters
category: Tech_Notes
tags:
  - Tech_Notes
  - Deveplement
status: in progress
created: 2026-11-15
updated: 2026-11-20
---
#### Automatic Pre-processing (Best to catch _any_ wild capitalization)

### In PowerShell (Natively Automatic)

PowerShell parameters are **natively case-insensitive** out of the box. You do not need to write any extra code to handle different capitalizations.

If you define a parameter like this:

PowerShell

```
param(
    [string]$ModelType = "ai-anime"
)
```

### 2. In Python (`argparse`)

In Python, `argparse` is case-sensitive by default.
If you want to automatically catch **any** random capitalization (like `-mODeltYpe` or `--MODELTYPE`) and normalize it _before_ `argparse` reads it, you can add a quick normalization loop to `sys.argv` right at the start of your script:

Python

```
import sys

# Automatically normalize any variant of --modeltype (regardless of casing or dashes) to '--ModelType'
sys.argv = [
    "--ModelType"
    if arg.lstrip("-").lower()
    in ["modeltype", "model_type", "type"]  # Add any flag names you want to normalize here
    else arg
    for arg in sys.argv
]

# Now standard argparse works seamlessly with whatever the user typed!
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ModelType", default="ai-anime")
args = parser.parse_args()
```

In Python, the standard convention for command-line parameters (using the built-in `argparse` library) follows POSIX and GNU command-line standards:

### 1. The Standard Convention

- **Long options (Double Dash `--`):** Used for full, descriptive parameter names (e.g., `--startfolder`, `--maxparallel`, `--debugmode`). If a name has multiple words, standard practice uses hyphens (kebab-case) like `--segment-length` or camelCase like `--SegmentLength`.
    
- **Short options (Single Dash `-`):** Used as quick, single-character abbreviations (e.g., `-s`, `-p`, `-d`).
    

### 2. How `argparse` Handles Them

When you define arguments in Python, you usually provide **both** the long and short versions so the user has options:

Python

```
parser.add_argument("--StartFolder", "-s", default=".", help="Working directory.")
```

### 3. Best Practices to Avoid Confusion

- **Always use double dashes (`--`) for full words:** `--startfolder`, `--type`, `--maxparallel`. If you only use a single dash with a long word (like `-startfolder`), Python's `argparse` will treat it as a bundle of single-character flags (`-s`, `-t`, `-a`, `-r`, etc.) and throw an error.
    
- **Use single dashes (`-`) strictly for single-letter shortcuts:** `-s`, `-t`, `-d`.