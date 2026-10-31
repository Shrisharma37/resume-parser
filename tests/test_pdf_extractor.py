import unittest
from io import BytesIO

from pypdf import PdfWriter

from resume_parser.extractors.pdf_extractor import (
    PDFExtractionError,
    extract_text_from_pdf,
)


class PDFExtractorTests(unittest.TestCase):
    def test_rejects_pdf_without_selectable_text(self):
        writer = PdfWriter()
        writer.add_blank_page(width=200, height=200)
        with self.assertRaisesRegex(PDFExtractionError, "No selectable text"):
            extract_text_from_pdf(_pdf_bytes(writer))

    def test_rejects_empty_file(self):
        with self.assertRaisesRegex(PDFExtractionError, "empty"):
            extract_text_from_pdf(b"")

    def test_rejects_invalid_pdf(self):
        with self.assertRaisesRegex(PDFExtractionError, "readable PDF"):
            extract_text_from_pdf(b"not a pdf")


def _pdf_bytes(writer):
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


if __name__ == "__main__":
    unittest.main()