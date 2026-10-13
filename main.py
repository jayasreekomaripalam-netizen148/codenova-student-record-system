"""Interactive CLI for Student Record Management System."""
from database import StudentDatabase


def show_students(students):
    if not students:
        print("\nNo student records found.")
        return
    print("\n{:<5} {:<22} {:<16} {:<30} {:>5}".format(
        "ID", "Name", "Roll No", "Email", "GPA"))
    print("-" * 83)
    for s in students:
        print("{:<5} {:<22} {:<16} {:<30} {:>5.2f}".format(
            s["id"], s["name"][:22], s["roll_no"][:16], s["email"][:30], s["gpa"]))


def ask_student_fields(existing=None):
    existing = existing or {}
    name = input(f"Name [{existing.get('name', '')}]: ").strip()
    roll = input(f"Roll number [{existing.get('roll_no', '')}]: ").strip()
    email = input(f"Email [{existing.get('email', '')}]: ").strip()
    gpa = input(f"GPA (0-10) [{existing.get('gpa', '')}]: ").strip()
    return (
        name or existing.get("name", ""),
        roll or existing.get("roll_no", ""),
        email or existing.get("email", ""),
        gpa or existing.get("gpa", ""),
    )


def main():
    db = StudentDatabase()
    actions = {
        "1": "Add student", "2": "View all students", "3": "Search students",
        "4": "Update student", "5": "Delete student", "0": "Exit",
    }
    while True:
        print("\n=== Student Record Management System ===")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                values = ask_student_fields()
                student = db.add_student(*values)
                print(f"Added student with database ID {student['id']}.")
            elif choice == "2":
                show_students(db.list_students())
            elif choice == "3":
                show_students(db.search_students(input("Search by name or roll number: ")))
            elif choice == "4":
                student_id = int(input("Database ID to update: "))
                existing = db.get_student(student_id)
                if not existing:
                    print("Student ID not found.")
                    continue
                print("Press Enter to keep each existing value.")
                if db.update_student(student_id, *ask_student_fields(existing)):
                    print("Student updated.")
                else:
                    print("Student ID not found.")
            elif choice == "5":
                student_id = int(input("Database ID to delete: "))
                if db.delete_student(student_id):
                    print("Student deleted.")
                else:
                    print("Student ID not found.")
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Choose one of the listed options.")
        except (ValueError, TypeError) as exc:
            print(f"Input error: {exc}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break


if __name__ == "__main__":
    main()
