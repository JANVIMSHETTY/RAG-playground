import fitz  # PyMuPDF

def extract_text_from_pdf(contents: bytes) -> str:
    doc = fitz.open(stream=contents, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
