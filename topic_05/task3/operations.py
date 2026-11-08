import functions


def input_number(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Помилка: введіть число.")


def input_numbers():
    a = input_number("Введіть перше число: ")
    b = input_number("Введіть друге число: ")
    return a, b


def add_operation():
    a, b = input_numbers()
    print(f"Результат: {a} + {b} = {functions.add(a, b)}")


def subtract_operation():
    a, b = input_numbers()
    print(f"Результат: {a} - {b} = {functions.subtract(a, b)}")


def multiply_operation():
    a, b = input_numbers()
    print(f"Результат: {a} * {b} = {functions.multiply(a, b)}")


def divide_operation():
    a, b = input_numbers()
    try:
        print(f"Результат: {a} / {b} = {functions.divide(a, b)}")
    except ZeroDivisionError as e:
        print(f"Помилка: {e}")