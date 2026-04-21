import io
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF file."""
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""

    for page in reader.pages:
        try:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        except Exception:
            # 🔥 FIX: Prevent crash on bad pages (no logic change)
            continue

    return text


def chunk_text(
    text: str,
    chunk_size: int = 1000,
    chunk_overlap: int = 200
) -> list[str]:
    """Splits text into overlapping chunks."""

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = text_splitter.split_text(text)
    return chunks