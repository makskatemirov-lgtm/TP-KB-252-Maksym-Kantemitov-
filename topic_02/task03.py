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


def calculator_match():
    a = float(input("Введіть перше число: "))
    op = input("Введіть операцію (+, -, *, /): ")
    b = float(input("Введіть друге число: "))

    match op:
        case "+":
            result = add(a, b)
        case "-":
            result = subtract(a, b)
        case "*":
            result = multiply(a, b)
        case "/":
            result = divide(a, b)
        case _:
            print("Невідома операція!")
            return

    if result is not None:
        print(f"Результат: {result}")


calculator_match()