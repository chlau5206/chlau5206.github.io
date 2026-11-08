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

# Configure root input and output
INPUT_ROOT = Path(r"C:\Users\charl_zt65sur\Doc\.src\.repos\github.io.bak\Notes_Input")      # change to your source root
OUTPUT_ROOT = Path(r"C:\Users\charl_zt65sur\Doc\.src\.repos\github.io.bak\Notes_MD_Output") # change to your target root

# Extensions we handle
TEXT_EXTS  = {".txt"}
RTF_EXTS   = {".rtf"}
HTML_EXTS  = {".html", ".htm", ".mht", ".mhtml"}
PDF_EXTS   = {".pdf"}
EPUB_EXTS  = {".epub"}
DOCX_EXTS  = {".docx"}
XPS_EXTS   = {".xps", "oxps"}

def run(cmd):
    """Run a command and return (success, stdout, stderr)."""
    try:
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        return (result.returncode == 0, result.stdout, result.stderr)
    except Exception as e:
        return (False, "", str(e))

def ensure_output_path(input_path: Path) -> Path:
    """Map input file path to output .md path under OUTPUT_ROOT."""
    rel = input_path.relative_to(INPUT_ROOT)
    out = OUTPUT_ROOT / rel
    return out.with_suffix(".md")

def convert_txt_to_md(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, dst)  # plain copy; .txt is already text
    print(f"[TXT] {src} -> {dst}")

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

def convert_pdf_to_md(src: Path, dst: Path):
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp_txt = dst.with_suffix(".tmp.txt")

    # First try pdftotext (text PDFs)
    ok, out, err = run(["pdftotext", str(src), str(tmp_txt)])
    if not ok:
        print(f"[WARN] pdftotext failed for {src}, consider OCR: {err}")
        return

    # Use pandoc to convert txt -> md
    convert_with_pandoc(tmp_txt, dst)
    tmp_txt.unlink(missing_ok=True)

def convert_xps_to_md(src: Path, dst: Path):
    # XPS -> PDF is not directly scriptable without extra tools.
    # For now, just log; you can manually convert XPS -> PDF and rerun.
    print(f"[XPS] {src} -> (manual XPS->PDF needed before MD)")

def process_file(path: Path):
    ext = path.suffix.lower()
    out_md = ensure_output_path(path)

    if ext in TEXT_EXTS:
        convert_txt_to_md(path, out_md)

    elif ext in RTF_EXTS:
        convert_with_pandoc(path, out_md)

    elif ext in HTML_EXTS:
        convert_with_pandoc(path, out_md)

    elif ext in EPUB_EXTS:
        convert_with_pandoc(path, out_md)

    elif ext in DOCX_EXTS:
        convert_with_pandoc(path, out_md)

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
