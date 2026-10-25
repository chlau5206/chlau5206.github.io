# Migration tool: convert mixed formats to Markdown  10/08/26
#=============================================================
# Assumptions:
# You install pandoc and pdftotext (from poppler).
# Optional: tesseract for OCR PDFs.
# You run this on Windows in a terminal.

import os
import subprocess
import shutil
from pathlib import Path
from uuid import uuid4

from bs4 import BeautifulSoup      # pip install beautifulsoup4
from docx import Document          # pip install python-docx

INPUT_ROOT = Path(r"C:\Users\charl_zt65sur\Doc\.src\.repos\chlau5206.github.io\Notes_Input")      # change to your source root
OUTPUT_ROOT = Path(r"C:\Users\charl_zt65sur\Doc\.src\.repos\chlau5206.github.io\Notes_MD_Output") # change to your target root

TEXT_EXTS  = {".txt"}
RTF_EXTS   = {".rtf"}
HTML_EXTS  = {".html", ".htm", ".mht", ".mhtml"}
PDF_EXTS   = {".pdf"}
EPUB_EXTS  = {".epub"}
DOCX_EXTS  = {".docx"}
XPS_EXTS   = {".xps"}

def run(cmd):
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except Exception as e:
        return (False, "", str(e))

def ensure_output_path(input_path: Path) -> Path:
    rel = input_path.relative_to(INPUT_ROOT)
    out = OUTPUT_ROOT / rel
    return out.with_suffix(".md")

def get_assets_dir(md_path: Path) -> Path:
    return md_path.parent / (md_path.stem + ".assets")

# ---------- TXT ----------

def convert_txt_to_md(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)
    print(f"[TXT] {src} -> {dst}")

# ---------- Pandoc generic ----------

def convert_with_pandoc(src: Path, dst: Path, extra_args=None):
    dst.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["pandoc", str(src), "-o", str(dst)]
    if extra_args:
        cmd.extend(extra_args)
    ok, out, err = run(cmd)
    if ok:
        print(f"[PANDOC] {src} -> {dst}")
    else:
        print(f"[ERROR] pandoc failed for {src}: {err}")

# ---------- PDF ----------

def convert_pdf_to_md(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp_txt = dst.with_suffix(".tmp.txt")

    ok, out, err = run(["pdftotext", str(src), str(tmp_txt)])
    if not ok:
        print(f"[WARN] pdftotext failed for {src}, consider OCR: {err}")
        return

    convert_with_pandoc(tmp_txt, dst)
    tmp_txt.unlink(missing_ok=True)

# ---------- XPS ----------

def convert_xps_to_md(src: Path, dst: Path):
    print(f"[XPS] {src} -> (manual XPS->PDF needed before MD)")

# ---------- DOCX with image extraction ----------

def convert_docx_to_md_with_images(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    assets_dir = get_assets_dir(dst)
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Extract images
    doc = Document(str(src))
    image_map = {}  # rId -> filename
    media_dir = src.parent / src.stem  # not used directly; we read from docx parts

    # python-docx stores images in doc.part.related_parts
    for rel_id, rel in doc.part.related_parts.items():
        if "image" in rel.content_type:
            ext = {
                "image/png": ".png",
                "image/jpeg": ".jpg",
                "image/gif": ".gif",
                "image/tiff": ".tif",
            }.get(rel.content_type, ".bin")
            img_name = f"{rel_id}_{uuid4().hex}{ext}"
            img_path = assets_dir / img_name
            with open(img_path, "wb") as f:
                f.write(rel.blob)
            image_map[rel_id] = img_name

    # Use pandoc to convert DOCX -> MD
    convert_with_pandoc(src, dst)

    # Optionally, you could post-process the MD to adjust image paths,
    # but pandoc usually writes relative paths that you can adapt later.

    print(f"[DOCX+IMG] {src} -> {dst}, images -> {assets_dir}")

# ---------- HTML with image extraction ----------

def convert_html_to_md_with_images(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    assets_dir = get_assets_dir(dst)
    assets_dir.mkdir(parents=True, exist_ok=True)

    # Parse HTML, copy local images into assets, rewrite src
    html_text = src.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html_text, "html.parser")

    for img in soup.find_all("img"):
        src_attr = img.get("src")
        if not src_attr:
            continue

        # Only handle local files (no http/https)
        if src_attr.startswith("http://") or src_attr.startswith("https://"):
            continue

        img_src_path = (src.parent / src_attr).resolve()
        if not img_src_path.exists():
            continue

        ext = img_src_path.suffix or ".png"
        new_name = f"{uuid4().hex}{ext}"
        new_path = assets_dir / new_name
        shutil.copy(img_src_path, new_path)

        img["src"] = f"{dst.stem}.assets/{new_name}"

    # Write modified HTML to temp file
    tmp_html = dst.with_suffix(".tmp.html")
    tmp_html.write_text(str(soup), encoding="utf-8")

    # Convert modified HTML -> MD
    convert_with_pandoc(tmp_html, dst)
    tmp_html.unlink(missing_ok=True)

    print(f"[HTML+IMG] {src} -> {dst}, images -> {assets_dir}")

# ---------- Dispatcher ----------

def process_file(path: Path):
    ext = path.suffix.lower()
    out_md = ensure_output_path(path)

    if ext in TEXT_EXTS:
        convert_txt_to_md(path, out_md)

    elif ext in RTF_EXTS:
        convert_with_pandoc(path, out_md)

    elif ext in HTML_EXTS:
        convert_html_to_md_with_images(path, out_md)

    elif ext in EPUB_EXTS:
        convert_with_pandoc(path, out_md)

    elif ext in DOCX_EXTS:
        convert_docx_to_md_with_images(path, out_md)

    elif ext in PDF_EXTS:
        convert_pdf_to_md(path, out_md)

    elif ext in XPS_EXTS:
        convert_xps_to_md(path, out_md)

    else:
        print(f"[SKIP] {path} (unsupported extension)")

def main():
    print(f"Input root : {INPUT_ROOT}")
    print(f"Output root: {OUTPUT_ROOT}\n")

    for root, dirs, files in os.walk(INPUT_ROOT):
        for name in files:
            src = Path(root) / name
            process_file(src)

    print("\nDone.")

if __name__ == "__main__":
    main()
