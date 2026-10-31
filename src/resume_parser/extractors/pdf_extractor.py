"""PDF-to-text extraction."""

from io import BytesIO

from pypdf import PdfReader
from pypdf.errors import PdfReadError

from resume_parser.utils.text_cleaner import clean_text


class PDFExtractionError(ValueError):
    """Raised when a PDF cannot provide usable text."""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from each page of a PDF byte sequence."""
    if not pdf_bytes:
        raise PDFExtractionError("The uploaded PDF is empty.")

    try:
        reader = PdfReader(BytesIO(pdf_bytes), strict=False)
    except PdfReadError as error:
        raise PDFExtractionError("The file is not a readable PDF.") from error

    if reader.is_encrypted:
        raise PDFExtractionError("This PDF is password-protected and cannot be read.")
    if not reader.pages:
        raise PDFExtractionError("The PDF does not contain any pages.")

    page_text = [page.extract_text() or "" for page in reader.pages]
    text = clean_text("\n\n".join(page_text))
    if not text:
        raise PDFExtractionError(
            "No selectable text was found. Scanned PDFs need OCR before they can be parsed."
        )
    return text