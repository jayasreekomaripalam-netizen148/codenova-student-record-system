"""SQLite persistence and validation for the Student Record Management System."""
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DEFAULT_DB = Path(__file__).with_name("students.db")


def validate_student(name, roll_no, email, gpa):
    name = str(name).strip()
    roll_no = str(roll_no).strip()
    email = str(email).strip()
    if not name:
        raise ValueError("Name cannot be empty.")
    if not roll_no:
        raise ValueError("Roll number cannot be empty.")
    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        raise ValueError("Enter a valid email address.")
    try:
        gpa = float(gpa)
    except (TypeError, ValueError):
        raise ValueError("GPA must be a number.") from None
    if not 0.0 <= gpa <= 10.0:
        raise ValueError("GPA must be between 0 and 10.")
    return name, roll_no, email, gpa


class StudentDatabase:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = str(db_path)
        self._create_table()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    @contextmanager
    def _connection(self):
        connection = self._connect()
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def _create_table(self):
        with self._connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    roll_no TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    email TEXT NOT NULL,
                    gpa REAL NOT NULL CHECK(gpa >= 0 AND gpa <= 10),
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
            """)

    @staticmethod
    def _dict(row):
        return dict(row) if row else None

    def add_student(self, name, roll_no, email, gpa):
        values = validate_student(name, roll_no, email, gpa)
        try:
            with self._connection() as conn:
                cursor = conn.execute(
                    "INSERT INTO students(name, roll_no, email, gpa) VALUES (?, ?, ?, ?)",
                    values,
                )
                student_id = cursor.lastrowid
            return self.get_student(student_id)
        except sqlite3.IntegrityError as exc:
            if "UNIQUE" in str(exc).upper():
                raise ValueError("That roll number already exists.") from None
            raise ValueError(f"Could not save student: {exc}") from None

    def list_students(self):
        with self._connection() as conn:
            rows = conn.execute(
                "SELECT * FROM students ORDER BY name COLLATE NOCASE, id"
            ).fetchall()
        return [dict(row) for row in rows]

    def get_student(self, student_id):
        with self._connection() as conn:
            row = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
        return self._dict(row)

    def search_students(self, query):
        query = str(query).strip()
        pattern = f"%{query}%"
        with self._connection() as conn:
            rows = conn.execute(
                """SELECT * FROM students
                   WHERE roll_no LIKE ? COLLATE NOCASE
                      OR name LIKE ? COLLATE NOCASE
                   ORDER BY name COLLATE NOCASE, id""",
                (pattern, pattern),
            ).fetchall()
        return [dict(row) for row in rows]

    def update_student(self, student_id, name, roll_no, email, gpa):
        values = validate_student(name, roll_no, email, gpa)
        try:
            with self._connection() as conn:
                cursor = conn.execute(
                    """UPDATE students SET name=?, roll_no=?, email=?, gpa=?
                       WHERE id=?""",
                    (*values, student_id),
                )
                if cursor.rowcount == 0:
                    return False
            return True
        except sqlite3.IntegrityError as exc:
            if "UNIQUE" in str(exc).upper():
                raise ValueError("That roll number already exists.") from None
            raise ValueError(f"Could not update student: {exc}") from None

    def delete_student(self, student_id):
        with self._connection() as conn:
            cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cursor.rowcount > 0
