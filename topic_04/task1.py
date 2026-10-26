
def add(a, b):
    return a + b
 
 
def subtract(a, b):
    return a - b
 
 
def multiply(a, b):
    return a * b
 
 
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Помилка: ділення на нуль неможливе!")
        return None
 
 
def input_number(prompt):
    while True:
        try:
            return float(input(prompt).replace(",", "."))
        except ValueError:
            print("Помилка: введіть коректне число!")
 
 
def input_operation():
    operations = {"+": add, "-": subtract, "*": multiply, "/": divide}
    while True:
        op = input("Оберіть операцію (+, -, *, /): ").strip()
        try:
            return op, operations[op]
        except KeyError:
            print("Помилка: невідома операція! Допустимі: +, -, *, /")
 
 
def main():
    print("Калькулятор")
    while True:
        try:
            a = input_number("Введіть перше число: ")
            op, func = input_operation()
            b = input_number("Введіть друге число: ")
 
            result = func(a, b)
            if result is not None:
                print(f"Результат: {a} {op} {b} = {result}")
 
            if input("Продовжити? (Enter - так, q - вийти): ").strip().lower() == "q":
                break
        except (KeyboardInterrupt, EOFError):
            print("\nРоботу завершено.")
            break
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
 
 
if __name__ == "__main__":
    main()
 