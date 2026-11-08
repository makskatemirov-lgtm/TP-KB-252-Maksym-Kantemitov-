import requests

API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
CURRENCIES = ["EUR", "USD", "PLN"]


def get_rate(currency):
    params = {"valcode": currency, "json": ""}
    response = requests.get(API_URL, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    if not data:
        raise ValueError(f"Курс для {currency} не знайдено.")
    return data[0]["rate"]


def get_currency():
    while True:
        currency = input(f"Тип валюти ({', '.join(CURRENCIES)}): ").strip().upper()
        if currency in CURRENCIES:
            return currency
        print("Помилка: непідтримувана валюта.")


def get_amount():
    while True:
        try:
            amount = float(input("Кількість: ").replace(",", "."))
            if amount < 0:
                print("Кількість не може бути від'ємною.")
                continue
            return amount
        except ValueError:
            print("Помилка: введіть число.")


def main():
    currency = get_currency()
    amount = get_amount()
    try:
        rate = get_rate(currency)
    except (requests.RequestException, ValueError, KeyError) as e:
        print(f"Не вдалося отримати курс: {e}")
        return
    result = amount * rate
    print(f"Курс НБУ: 1 {currency} = {rate} UAH")
    print(f"{amount} {currency} = {result:.2f} UAH")


if __name__ == "__main__":
    main()