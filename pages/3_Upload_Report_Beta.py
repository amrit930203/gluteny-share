
import streamlit as st
from datetime import date
import os

REPORT_FILE = "report_memory.txt"

# --- Upload style ---
def apply_upload_style():
    st.markdown("""
    <style>
    /* Set entire page background to premium yellow */
    html, body, .stApp {
        background-color: #fff8dc !important;
    }
    .stFileUploader {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 1rem;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0,255,100,0.1);
        backdrop-filter: blur(8px);
        margin-top: 1rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }

    .stFileUploader label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 1rem;
    }

    .stFileUploader .uploadedFileName {
        color: #ffffff;
    }

    .stFileUploader .css-1cpxqw2 {
        background-color: #2ecc71;
        color: white;
        border-radius: 8px;
        padding: 0.4rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .stFileUploader .css-1cpxqw2:hover {
        background-color: #27ae60;
        transform: scale(1.03);
    }

    .stFileUploader svg {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

# --- PDF Extraction ---
def extract_text_from_pdf(file):
    try:
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- Page UI ---
st.set_page_config(page_title="📁 Upload Medical Reports (Beta)", layout="centered")
st.title("📁 Upload Medical Reports (Beta)")
apply_upload_style()

uploaded_file = st.file_uploader("Upload a PDF or TXT report", type=["pdf", "txt"])

if uploaded_file:
    if uploaded_file.type == "text/plain":
        new_text = uploaded_file.read().decode("utf-8")
    else:
        new_text = extract_text_from_pdf(uploaded_file)

    with open(REPORT_FILE, "a") as f:
        f.write("\n\n" + new_text.strip())

    st.success("✅ Report uploaded and remembered")
    st.rerun()

if os.path.exists(REPORT_FILE):
    with st.expander("🧠 View remembered report data"):
        with open(REPORT_FILE, "r") as f:
            st.text_area("Stored Report Info", value=f.read(), height=200)
