# List [Item1, Item2, Item3]
# Item {"name": "Jon", "phone": "0631234567", "email": "jon@gmail.com", "group": "kb-242"}
#
# Usage: python lab2.py lab2.csv

import csv
import re
from sys import argv

FIELDNAMES = ["name", "phone", "email", "group"]
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")

# list is always kept sorted by name (case-insensitive)
students = []


# ---------------------------------------------------------------- files

def load_students(file_name):
    """Read students from a CSV file and return a list sorted by name."""
    result = []
    with open(file_name, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            result.append({
                "name": row["name"],
                "phone": row["phone"],
                "email": row["email"],
                "group": row["group"],
            })
    result.sort(key=lambda item: item["name"].lower())
    return result


def save_students(file_name, items):
    """Write students to a CSV file (with header row)."""
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writeheader()
        for item in items:
            writer.writerow(item)


# ----------------------------------------------------------- validation

def is_valid_phone(value):
    """Phone is valid if it contains exactly 10 digits."""
    return value.isdigit() and len(value) == 10


def is_valid_email(value):
    """Email is valid if it matches EMAIL_PATTERN."""
    return EMAIL_PATTERN.match(value) is not None


# ---------------------------------------------------------------- input

def input_non_empty(prompt):
    """Ask until the user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Value cannot be empty")


def input_phone(prompt):
    """Ask until the user enters a valid phone (digits only, 10 digits)."""
    while True:
        value = input(prompt).strip()
        if is_valid_phone(value):
            return value
        print("Phone must contain exactly 10 digits, e.g. 0631234567")


def input_email(prompt):
    """Ask until the user enters a valid email."""
    while True:
        value = input(prompt).strip()
        if is_valid_email(value):
            return value
        print("Wrong email format, e.g. name@gmail.com")


def read_student(prefix=""):
    """Read all student fields from the user and return a new item."""
    name = input_non_empty(f"Please enter {prefix}student name: ")
    phone = input_phone(f"Please enter {prefix}student phone: ")
    email = input_email(f"Please enter {prefix}student email: ")
    group = input_non_empty(f"Please enter {prefix}student group: ")
    return {"name": name, "phone": phone, "email": email, "group": group}


# ------------------------------------------------------------ list logic

def print_all_list():
    """Print all students."""
    if not students:
        print("List is empty")
        return
    for s in students:
        print(f"Student name is {s['name']},  Phone is {s['phone']},  "
              f"Email is {s['email']},  Group is {s['group']}")


def find_insert_position(name):
    """Find the position that keeps the list sorted by name."""
    position = 0
    for item in students:
        if name.lower() > item["name"].lower():
            position += 1
        else:
            break
    return position


def find_index_by_name(name):
    """Return index of the first student with the given name or -1."""
    for i, item in enumerate(students):
        if item["name"].lower() == name.lower():
            return i
    return -1


def insert_student(item):
    """Insert item keeping the list sorted. Return the position."""
    position = find_insert_position(item["name"])
    students.insert(position, item)
    return position


def remove_student(name):
    """Remove the first student with the given name. Return index or -1."""
    index = find_index_by_name(name)
    if index != -1:
        del students[index]
    return index


def replace_student(name, new_item):
    """Replace the student with the given name. Return True if found."""
    if remove_student(name) == -1:
        return False
    insert_student(new_item)
    return True


# --------------------------------------------------------------- actions

def add_new_element():
    insert_student(read_student())
    print("New element has been added")


def delete_element():
    name = input_non_empty("Please enter name to be deleted: ")
    index = remove_student(name)
    if index == -1:
        print("Element was not found")
        return
    print(f"Element at position {index} has been deleted")


def update_element():
    name = input_non_empty("Please enter name to be updated: ")
    if find_index_by_name(name) == -1:
        print("Element was not found")
        return
    replace_student(name, read_student("new "))
    print("Element has been updated")


def main():
    global students

    if len(argv) < 2:
        print("Usage: python lab2.py <file.csv>")
        return
    file_name = argv[1]
    try:
        students = load_students(file_name)
    except FileNotFoundError:
        print(f"File {file_name} was not found")
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
                add_new_element()
                print_all_list()
            case "u":
                print("Existing element will be updated")
                update_element()
                print_all_list()
            case "d":
                print("Element will be deleted")
                delete_element()
                print_all_list()
            case "p":
                print("List will be printed")
                print_all_list()
            case "x":
                save_students(file_name, students)
                print(f"List has been saved to {file_name}")
                print("Exit()")
                break
            case _:
                print("Wrong choice")


if __name__ == "__main__":
    main()
