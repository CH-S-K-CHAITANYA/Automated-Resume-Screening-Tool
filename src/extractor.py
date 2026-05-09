"""
extractor.py
============
Handles text extraction from PDF and DOCX resume files.
Uses pdfplumber for PDFs and python-docx for Word documents.
"""

import os
import pdfplumber
from docx import Document


def extract_text_from_pdf(filepath: str) -> str:
    """
    Extract all text from a PDF file using pdfplumber.
    pdfplumber handles complex layouts better than PyPDF2.
    
    Args:
        filepath: Full path to the PDF file.
    Returns:
        Extracted text as a single string.
    """
    text = ""
    try:
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:  # some pages may be empty
                    text += page_text + "\n"
    except Exception as e:
        print(f"  [WARNING] Could not read PDF '{os.path.basename(filepath)}': {e}")
    return text.strip()


def extract_text_from_docx(filepath: str) -> str:
    """
    Extract all text from a DOCX file using python-docx.
    
    Args:
        filepath: Full path to the DOCX file.
    Returns:
        Extracted text as a single string.
    """
    text = ""
    try:
        doc = Document(filepath)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        text = "\n".join(paragraphs)
    except Exception as e:
        print(f"  [WARNING] Could not read DOCX '{os.path.basename(filepath)}': {e}")
    return text.strip()


def extract_text_from_txt(filepath: str) -> str:
    """
    Extract text from a plain .txt file.
    
    Args:
        filepath: Full path to the .txt file.
    Returns:
        Raw text content.
    """
    text = ""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    except Exception as e:
        print(f"  [WARNING] Could not read TXT '{os.path.basename(filepath)}': {e}")
    return text.strip()


def extract_text(filepath: str) -> str:
    """
    Smart dispatcher: detects file extension and calls the right extractor.
    Supports .pdf, .docx, and .txt files.
    
    Args:
        filepath: Full path to the resume file.
    Returns:
        Extracted raw text.
    """
    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".pdf":
        return extract_text_from_pdf(filepath)
    elif ext == ".docx":
        return extract_text_from_docx(filepath)
    elif ext == ".txt":
        return extract_text_from_txt(filepath)
    else:
        print(f"  [SKIP] Unsupported format: {os.path.basename(filepath)}")
        return ""


def load_all_resumes(resumes_dir: str) -> dict:
    """
    Load and extract text from ALL resume files in a directory.
    
    Args:
        resumes_dir: Path to the folder containing resume files.
    Returns:
        Dictionary mapping filename → extracted text.
    """
    resume_texts = {}
    supported = (".pdf", ".docx", ".txt")

    files = [f for f in os.listdir(resumes_dir) if f.lower().endswith(supported)]

    if not files:
        print(f"[ERROR] No resumes found in '{resumes_dir}'. Add PDF/DOCX/TXT files.")
        return {}

    print(f"\n📂 Found {len(files)} resume(s) in '{resumes_dir}'")
    for filename in sorted(files):
        full_path = os.path.join(resumes_dir, filename)
        print(f"  ✅ Extracting: {filename}")
        text = extract_text(full_path)
        if text:
            resume_texts[filename] = text
        else:
            print(f"  ⚠️  Empty text extracted from: {filename}")

    return resume_texts
