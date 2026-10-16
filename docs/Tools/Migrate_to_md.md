Below is a polished, production‑ready **README.md** you can drop directly into your GitHub repo for your Markdown Migration Tool. It’s structured for clarity, long‑term maintainability, and GitHub Pages friendliness.

# 📘 Markdown Migration Tool

Convert mixed document formats into future‑proof **Markdown (.md)** for Obsidian vaults, GitHub Pages (MkDocs), and long‑term personal knowledge bases.

This tool walks an input directory, detects supported file types, and converts each file into Markdown while preserving folder structure.

## 🧩 Features

- Converts multiple formats to Markdown:
    
    - TXT
        
    - RTF
        
    - HTML / HTM / MHT / MHTML
        
    - PDF (text‑based)
        
    - EPUB
        
    - DOCX
        
    - XPS → (manual PDF step required)
        
- Preserves directory structure
    
- Creates parallel Markdown output tree
    
- Uses Pandoc for high‑quality conversion
    
- Uses Poppler (`pdftotext`) for PDF extraction
    
- Optional OCR support for scanned PDFs
    
- Designed for Obsidian + MkDocs workflows
    

## 📦 Requirements

### **Python 3.8+**

Install from: [https://www.python.org/](https://www.python.org/?utm_source=copilot.com "www.python.org")

### **Pandoc** (required)

Pandoc performs most conversions. Install: `https://pandoc.org/installing.html` [(pandoc.org in Bing)](https://www.bing.com/search?q=%22https%3A%2F%2Fpandoc.org%2Finstalling.html%22&utm_source=copilot.com "www.bing.com")

Verify:

Code

```
pandoc --version
```

### **Poppler** (required for PDF → text)

Install Windows binaries: `https://github.com/oschwartz10612/poppler-windows/releases/` [(github.com in Bing)](https://www.bing.com/search?q=%22https%3A%2F%2Fgithub.com%2Foschwartz10612%2Fpoppler-windows%2Freleases%2F%22&utm_source=copilot.com "www.bing.com")

Add `poppler/bin` to PATH.

Verify:

Code

```
pdftotext -v
```

### **Tesseract OCR** (optional, for scanned PDFs)

Install: `https://github.com/tesseract-ocr/tesseract` [(github.com in Bing)](https://www.bing.com/search?q=%22https%3A%2F%2Fgithub.com%2Ftesseract-ocr%2Ftesseract%22&utm_source=copilot.com "www.bing.com")

Verify:

Code

```
tesseract --version
```

## 📁 Folder Structure

### **Input directory**

Place your mixed-format documents here:

Code

```
C:\Notes_Input\
    Recipes\
    Tech\
    Home\
    Health\
```

### **Output directory**

The tool creates:

Code

```
C:\Notes_MD_Output\
    Recipes\
    Tech\
    Home\
    Health\
```

Each file becomes `.md` with the same relative path.

## ▶️ Usage

### **1. Configure paths**

Edit the top of the script:

python

```
INPUT_ROOT = Path(r"C:\Notes_Input")
OUTPUT_ROOT = Path(r"C:\Notes_MD_Output")
```

### **2. Run the tool**

From PowerShell or CMD:

Code

```
python migrate_to_md.py
```

### **3. Review output**

Converted Markdown files appear under:

Code

```
C:\Notes_MD_Output\
```

### **4. Move output into your Obsidian vault**

Organize notes into folders, add images, and begin linking inside Obsidian.

### **5. Publish via MkDocs (optional)**

Use MkDocs + GitHub Pages to create a public documentation site.

## 🧪 Conversion Examples

### TXT → MD

Plain copy.

### RTF → MD

Code

```
pandoc input.rtf -o input.md
```

### HTML / MHT → MD

Code

```
pandoc input.html -o input.md
```

### PDF → MD

Code

```
pdftotext input.pdf temp.txt
pandoc temp.txt -o input.md
```

### EPUB → MD

Code

```
pandoc input.epub -o input.md
```

### DOCX → MD

Code

```
pandoc input.docx -o input.md
```

### XPS → MD

Manual step:

1. Print XPS → PDF
    
2. Convert PDF → MD
    

## ⚠️ Limitations

- Scanned PDFs require OCR (Tesseract).
    
- XPS must be converted to PDF manually.
    
- Images inside DOCX/HTML/PDF are not extracted in this version.
    
- Tables convert best from DOCX/HTML; RTF/TXT may lose formatting.
    
- MHT conversion depends on Pandoc’s HTML extraction quality.
    

## 🚀 Recommended Workflow

1. Convert all documents to Markdown using this tool.
    
2. Move Markdown files into your Obsidian vault.
    
3. Organize notes into a simple folder structure.
    
4. Sync selected folders to GitHub.
    
5. Use MkDocs to publish your public wiki.
    

## 📄 License

MIT License (or your preferred license).
