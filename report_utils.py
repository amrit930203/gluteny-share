# utils/report_utils.py
from config import REPORT_FILE
import os

def append_report_text(text):
    with open(REPORT_FILE, "a") as f:
        f.write("\n\n" + text.strip())

def get_report_memory():
    if os.path.exists(REPORT_FILE):
        with open(REPORT_FILE, "r") as f:
            return f.read()
    return ""

def extract_text_from_pdf(file):
    import PyPDF2
    reader = PyPDF2.PdfReader(file)
    return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])