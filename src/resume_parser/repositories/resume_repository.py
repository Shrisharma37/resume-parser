"""Explicit local persistence for parsed resumes."""

import json
import sqlite3
from contextlib import closing
from pathlib import Path

from resume_parser.config import DEFAULT_DATABASE
from resume_parser.models.resume import Resume


class ResumeRepository:
    """Store parsed resume data in a local SQLite database."""

    def __init__(self, database_path: Path | str = DEFAULT_DATABASE) -> None:
        self.database_path = Path(database_path)
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        with closing(sqlite3.connect(self.database_path)) as connection, connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS resumes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    name TEXT,
                    data_json TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def save(self, resume: Resume) -> int:
        """Save parsed data and return its database ID."""
        with closing(sqlite3.connect(self.database_path)) as connection, connection:
            cursor = connection.execute(
                "INSERT INTO resumes (filename, name, data_json) VALUES (?, ?, ?)",
                (
                    resume.filename,
                    resume.name,
                    json.dumps(resume.to_dict(), ensure_ascii=False),
                ),
            )
            return int(cursor.lastrowid)

    def get(self, resume_id: int) -> Resume | None:
        """Load a resume by ID, returning None when it does not exist."""
        with closing(sqlite3.connect(self.database_path)) as connection, connection:
            row = connection.execute(
                "SELECT data_json FROM resumes WHERE id = ?", (resume_id,)
            ).fetchone()
        return Resume.from_dict(json.loads(row[0])) if row else None

    def list_resumes(self) -> list[dict[str, str | int | None]]:
        """Return saved resume metadata without exposing stored resume contents."""
        with closing(sqlite3.connect(self.database_path)) as connection, connection:
            rows = connection.execute(
                "SELECT id, filename, name, created_at FROM resumes ORDER BY id DESC"
            ).fetchall()
        return [
            {"id": row[0], "filename": row[1], "name": row[2], "created_at": row[3]}
            for row in rows
        ]

    def delete(self, resume_id: int) -> bool:
        """Delete a saved resume and report whether a row was removed."""
        with closing(sqlite3.connect(self.database_path)) as connection, connection:
            cursor = connection.execute("DELETE FROM resumes WHERE id = ?", (resume_id,))
            return cursor.rowcount > 0