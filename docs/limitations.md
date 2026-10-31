# Limitations

- Only PDF files with selectable text are supported. Image-only/scanned PDFs
  require OCR, which is not included.
- Contact and name extraction use regular expressions and simple heuristics;
  results can be incomplete or incorrect for unusual layouts.
- Section parsing recognizes common headings and captures text until the next
  recognized heading. It does not preserve complex visual layout or columns.
- Skill detection is limited to the names and aliases in `data/skills.json`.
  Extend that file to cover more domains and spelling variants.
- Job matching compares recognized skills only. The percentage is not a
  semantic assessment of experience, proficiency, or candidate suitability.
- Local SQLite storage contains personal information and is not encrypted.
  Save only on a trusted device and remove the database when it is no longer
  needed.