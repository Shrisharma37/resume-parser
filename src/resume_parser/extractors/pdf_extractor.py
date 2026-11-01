"""PDF-to-text extraction using PyMuPDF."""
import fitz

from resume_parser.utils.text_cleaner import clean_text


class PDFExtractionError(ValueError):
    """Raised when a PDF cannot provide usable text."""


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract selectable text from all pages of a PDF byte sequence."""
    if not pdf_bytes:
        raise PDFExtractionError("The uploaded PDF is empty.")
    try:
        document = fitz.open(stream=pdf_bytes, filetype="pdf")
        if document.needs_pass:
            raise PDFExtractionError("This PDF is password-protected and cannot be read.")
        if document.page_count == 0:
            raise PDFExtractionError("The PDF does not contain any pages.")
        text = clean_text("\\n\\n".join(page.get_text("text") for page in document))
        document.close()
    except PDFExtractionError:
        raise
    except Exception as error:
        raise PDFExtractionError("The file is not a readable PDF.") from error

    if not text:
        raise PDFExtractionError(
            "No selectable text was found. This appears to be a scanned PDF; OCR is required."
        )
    return text
