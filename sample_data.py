"""Insert a small demonstration dataset without duplicating existing roll numbers."""
from database import StudentDatabase

SAMPLE_STUDENTS = [
    ("Ananya Rao", "CN101", "ananya@example.com", 8.7),
    ("Rahul Kumar", "CN102", "rahul@example.com", 7.9),
    ("Meera Das", "CN103", "meera@example.com", 9.2),
]


def main():
    db = StudentDatabase()
    for student in SAMPLE_STUDENTS:
        try:
            db.add_student(*student)
            print(f"Added {student[1]}")
        except ValueError as exc:
            print(f"Skipped {student[1]}: {exc}")


if __name__ == "__main__":
    main()
