# List [Item1, Item2, Item3]
# Item {"name": "Jon", "phone": "0631234567", "email": "jon@gmail.com", "group": "kb-242"}

import re

# already sorted list (by name, case-insensitive)
students = [
    {"name": "Bob", "phone": "0631234567", "email": "bob@gmail.com", "group": "kb-242"},
    {"name": "Emma", "phone": "0631234567", "email": "emma@gmail.com", "group": "kb-242"},
    {"name": "Jon", "phone": "0631234567", "email": "jon@gmail.com", "group": "kb-242"},
    {"name": "Zak", "phone": "0631234567", "email": "zak@gmail.com", "group": "kb-242"},
]

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


def print_all_list():
    """Print all students."""
    if not students:
        print("List is empty")
        return
    for s in students:
        print(f"Student name is {s['name']},  Phone is {s['phone']},  "
              f"Email is {s['email']},  Group is {s['group']}")


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
        if value.isdigit() and len(value) == 10:
            return value
        print("Phone must contain exactly 10 digits, e.g. 0631234567")


def input_email(prompt):
    """Ask until the user enters a valid email."""
    while True:
        value = input(prompt).strip()
        if EMAIL_PATTERN.match(value):
            return value
        print("Wrong email format, e.g. name@gmail.com")


def read_student(prefix=""):
    """Read all student fields from the user and return a new item."""
    name = input_non_empty(f"Please enter {prefix}student name: ")
    phone = input_phone(f"Please enter {prefix}student phone: ")
    email = input_email(f"Please enter {prefix}student email: ")
    group = input_non_empty(f"Please enter {prefix}student group: ")
    return {"name": name, "phone": phone, "email": email, "group": group}


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


def add_new_element():
    new_item = read_student()
    students.insert(find_insert_position(new_item["name"]), new_item)
    print("New element has been added")


def delete_element():
    name = input_non_empty("Please enter name to be deleted: ")
    index = find_index_by_name(name)
    if index == -1:
        print("Element was not found")
        return
    del students[index]
    print(f"Element at position {index} has been deleted")


def update_element():
    name = input_non_empty("Please enter name to be updated: ")
    index = find_index_by_name(name)
    if index == -1:
        print("Element was not found")
        return
    update_item = read_student("new ")
    del students[index]
    students.insert(find_insert_position(update_item["name"]), update_item)
    print("Element has been updated")


def main():
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
                print("Exit()")
                break
            case _:
                print("Wrong choice")


if __name__ == "__main__":
    main()