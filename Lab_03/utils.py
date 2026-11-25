import csv

from student import Student
from student_list import StudentList

FIELDNAMES = ["name", "phone", "email", "group"]


class CsvStorage:
    """Reads and writes the group list from/to a CSV file."""

    def __init__(self, file_name):
        self.file_name = file_name

    def load(self):
        """Read the file and return StudentList."""
        result = StudentList()
        with open(self.file_name, newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                result.add(Student.from_dict(row))
        return result

    def save(self, student_list):
        """Write StudentList to the file (with header row)."""
        with open(self.file_name, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()
            for student in student_list:
                writer.writerow(student.to_dict())
