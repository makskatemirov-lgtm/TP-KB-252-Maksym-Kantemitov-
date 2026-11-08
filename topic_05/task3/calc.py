import functions
import operations

MENU = """
=== Калькулятор ===
1 - Додавання
2 - Віднімання
3 - Множення
4 - Ділення
0 - Вихід
"""

ACTIONS = {
    "1": operations.add_operation,
    "2": operations.subtract_operation,
    "3": operations.multiply_operation,
    "4": operations.divide_operation,
}


def main():
    while True:
        print(MENU)
        choice = input("Оберіть дію: ").strip()
        if choice == "0":
            print("До побачення!")
            break
        action = ACTIONS.get(choice)
        if action:
            action()
        else:
            print("Невірний вибір, спробуйте ще раз.")


if __name__ == "__main__":
    main()