# src/utils.py

import json
import os
from PyPDF2 import PdfReader

def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ''.join(page.extract_text() for page in reader.pages)
        return text
    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return None


def load_json_keywords(file_path='src/utils/job_keywords.json'):
    """Load the job_keywords.json file and return its contents as a dictionary."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Error loading JSON file {file_path}: {e}")
        return {}
