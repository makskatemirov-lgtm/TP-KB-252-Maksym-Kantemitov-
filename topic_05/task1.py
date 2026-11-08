import random

CHOICES = ["stone", "scissor", "paper"]
WINS = {"stone": "scissor", "scissor": "paper", "paper": "stone"}


def get_user_choice():
    while True:
        choice = input("Ваш вибір (stone, scissor, paper): ").strip().lower()
        if choice in CHOICES:
            return choice
        print("Помилка: введіть одне зі значень stone, scissor, paper.")


def get_winner(user, computer):
    if user == computer:
        return "Нічия!"
    if WINS[user] == computer:
        return "Ви перемогли!"
    return "Комп'ютер переміг!"


def main():
    user = get_user_choice()
    computer = random.choice(CHOICES)
    print(f"Ви: {user}")
    print(f"Комп'ютер: {computer}")
    print(get_winner(user, computer))


if __name__ == "__main__":
    main()