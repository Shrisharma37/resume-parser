"""Project paths and runtime limits."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
SKILLS_FILE = DATA_DIR / "skills.json"
DEFAULT_DATABASE = DATA_DIR / "resumes.sqlite3"
MAX_UPLOAD_SIZE_MB = 10