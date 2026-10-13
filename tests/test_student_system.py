import tempfile
import unittest
from pathlib import Path
from database import StudentDatabase


class StudentSystemTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db = StudentDatabase(Path(self.temp.name) / "test.db")

    def tearDown(self):
        self.temp.cleanup()

    def add(self, name="Asha Rao", roll="R101", email="asha@example.com", gpa=8.5):
        return self.db.add_student(name, roll, email, gpa)

    def test_add_and_persistence(self):
        student = self.add()
        reopened = StudentDatabase(self.db.db_path)
        self.assertEqual(reopened.get_student(student["id"])["roll_no"], "R101")

    def test_duplicate_roll_rejected_case_insensitively(self):
        self.add()
        with self.assertRaises(ValueError):
            self.add(name="Other", roll="r101", email="other@example.com")

    def test_validation(self):
        with self.assertRaises(ValueError):
            self.add(email="not-an-email")
        with self.assertRaises(ValueError):
            self.add(gpa=11)

    def test_partial_case_insensitive_search(self):
        self.add(name="Jaya Komaripalem", roll="ABC123")
        self.assertEqual(len(self.db.search_students("jAyA")), 1)
        self.assertEqual(len(self.db.search_students("bc1")), 1)

    def test_update_and_delete(self):
        student = self.add()
        self.assertTrue(self.db.update_student(student["id"], "Asha K", "R102", "asha.k@example.com", 9))
        self.assertEqual(self.db.get_student(student["id"])["roll_no"], "R102")
        self.assertTrue(self.db.delete_student(student["id"]))
        self.assertIsNone(self.db.get_student(student["id"]))


if __name__ == "__main__":
    unittest.main()
