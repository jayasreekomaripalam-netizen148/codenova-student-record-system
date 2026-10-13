# Student Record Management System

CodeNova Python Programming Internship — Task 1.

A command-line student database using Python and SQLite. It supports adding, listing, searching, updating and deleting records, with validation and persistent storage.

## Features
- Full CRUD (create, read, update, delete).
- SQLite storage; records remain after restarting the program.
- Unique roll numbers (case-insensitive).
- Search by partial name or roll number, case-insensitively.
- Email format validation and GPA validation from 0 to 10.
- Friendly handling of invalid input and duplicate roll numbers.
- Demonstration dataset and automated unit tests.

## Requirements
Python 3.9 or later. No third-party dependencies.

## Run in Termux
```bash
cd ~/codenova-internship/student-record-system
python main.py
```

To add demonstration records:
```bash
python sample_data.py
```
The database file `students.db` is created automatically in this folder.

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Database and validation
The `students` table uses an auto-incrementing integer primary key and a unique, case-insensitive roll number. Values are passed to SQLite as parameters rather than assembled into SQL strings. GPA is restricted to 0–10, and email must have a basic `name@domain.tld` shape. The email check is intentionally lightweight, not a guarantee that an address exists.

## Screenshots for submission
Capture these terminal screens using your phone's screenshot function:
1. Main menu after running `python main.py`.
2. Adding a student successfully.
3. Viewing records and searching with a partial name.
4. Duplicate roll number or invalid GPA showing a friendly error.
5. Automated tests passing.

Do not include private student information in screenshots. Use the sample records.

## GitHub publishing
Create a **public** repository named `codenova-student-record-system` on GitHub, then run:
```bash
git init
git add main.py database.py sample_data.py requirements.txt README.md tests
git commit -m "Build Student Record Management System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/codenova-student-record-system.git
git push -u origin main
```
Replace `YOUR_USERNAME` with your GitHub username. Do not commit `students.db` if it contains real personal information. Add it to `.gitignore` if needed.
