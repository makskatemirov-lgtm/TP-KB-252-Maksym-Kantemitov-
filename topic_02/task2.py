def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        print("Помилка: ділення на нуль!")
        return None
    return a / b


def calculator_if_else():
    a = float(input("Введіть перше число: "))
    op = input("Введіть операцію (+, -, *, /): ")
    b = float(input("Введіть друге число: "))

    if op == "+":
        result = add(a, b)
    elif op == "-":
        result = subtract(a, b)
    elif op == "*":
        result = multiply(a, b)
    elif op == "/":
        result = divide(a, b)
    else:
        print("Невідома операція!")
        return

    if result is not None:
        print(f"Результат: {result}")


calculator_if_else()