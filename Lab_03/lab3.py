# Usage: python lab3.py lab3.csv

from sys import argv

from student import Student
from student_list import StudentList
from utils import CsvStorage


def input_non_empty(prompt):
    """Ask until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty")


def input_phone(prompt):
    """Ask until the user enters a valid phone (10 digits)."""
    while True:
        value = input(prompt).strip()
        if Student.is_valid_phone(value):
            return value
        print("Phone must contain exactly 10 digits, e.g. 0631234567")


def input_email(prompt):
    """Ask until the user enters a valid email."""
    while True:
        value = input(prompt).strip()
        if Student.is_valid_email(value):
            return value
        print("Wrong email format, e.g. name@gmail.com")


def read_student(prefix=""):
    """Read all fields from the user and return a new Student."""
    name = input_non_empty(f"Please enter {prefix}student name: ")
    phone = input_phone(f"Please enter {prefix}student phone: ")
    email = input_email(f"Please enter {prefix}student email: ")
    group = input_non_empty(f"Please enter {prefix}student group: ")
    return Student(name, phone, email, group)


def add_new_element(students):
    students.add(read_student())
    print("New element has been added")


def delete_element(students):
    name = input_non_empty("Please enter name to be deleted: ")
    index = students.delete(name)
    if index == -1:
        print("Element was not found")
        return
    print(f"Element at position {index} has been deleted")


def update_element(students):
    name = input_non_empty("Please enter name to be updated: ")
    if students.find_index(name) == -1:
        print("Element was not found")
        return
    students.update(name, read_student("new "))
    print("Element has been updated")


def main():
    if len(argv) < 2:
        print("Usage: python lab3.py <file.csv>")
        return
    storage = CsvStorage(argv[1])
    try:
        students = storage.load()
    except FileNotFoundError:
        print(f"File {argv[1]} was not found")
        return
    except KeyError as error:
        print(f"Wrong CSV format, column {error} is missing")
        return

    while True:
        choice = input(
            "Please specify the action [ C create, U update, D delete, P print, X exit ] "
        ).strip().lower()
        match choice:
            case "c":
                print("New element will be created:")
                add_new_element(students)
                students.print_all()
            case "u":
                print("Existing element will be updated")
                update_element(students)
                students.print_all()
            case "d":
                print("Element will be deleted")
                delete_element(students)
                students.print_all()
            case "p":
                print("List will be printed")
                students.print_all()
            case "x":
                storage.save(students)
                print(f"List has been saved to {argv[1]}")
                print("Exit()")
                break
            case _:
                print("Wrong choice")


if __name__ == "__main__":
    main()
