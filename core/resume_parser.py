import io
import pdfplumber


def extract_text_from_pdf(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages = [(p.extract_text() or "") for p in pdf.pages]
    return "\n".join([p for p in pages if p.strip()]).strip()
