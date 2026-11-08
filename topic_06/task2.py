students = [
    {"name": "Олег", "grade": 82},
    {"name": "Марк", "grade": 95},
    {"name": "Інна", "grade": 74},
    {"name": "Анна", "grade": 88},
    {"name": "Павло", "grade": 91}
]

print("List:")
for student in students:
    print(student)

sorted_by_grade = sorted(students, key=lambda x: x["grade"])
print("Sorting by grades:")
for student in sorted_by_grade:
    print(student)

sorted_by_name = sorted(students, key=lambda x: x["name"])
print("\nSorting by name:")
for student in sorted_by_name:
    print(student)