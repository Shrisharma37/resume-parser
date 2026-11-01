"""Batch-test every PDF in a folder and write one JSON result per resume.

Usage:
    python scripts/test_resumes.py sample_resumes
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from resume_parser.extractors.pdf_extractor import PDFExtractionError
from resume_parser.services.resume_parser_service import parse_resume


def main() -> int:
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("sample_resumes")
    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        print("Create the folder and put your test PDF files inside it.")
        return 1

    output_folder = folder / "parsed_output"
    output_folder.mkdir(exist_ok=True)
    pdf_files = sorted(folder.glob("*.pdf"))

    if not pdf_files:
        print(f"No PDF files found in: {folder}")
        return 1

    passed = 0
    for pdf_path in pdf_files:
        try:
            resume = parse_resume(pdf_path.read_bytes(), filename=pdf_path.name)
            output_path = output_folder / f"{pdf_path.stem}.json"
            output_path.write_text(
                json.dumps(resume.to_export_dict(), indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(f"[OK] {pdf_path.name} -> {output_path}")
            print(
                "     Name:", resume.name or "Not found",
                "| Education blocks:", len(resume.to_export_dict()["education"]),
                "| Languages:", ", ".join(resume.languages) or "Not found",
                "| Summary:", "Found" if resume.sections.get("summary") else "Not found",
            )
            passed += 1
        except (PDFExtractionError, OSError) as error:
            print(f"[ERROR] {pdf_path.name}: {error}")

    print(f"\\nFinished: {passed}/{len(pdf_files)} PDFs parsed.")
    print(f"JSON files are saved in: {output_folder}")
    return 0 if passed == len(pdf_files) else 2


if __name__ == "__main__":
    raise SystemExit(main())
