def calculator():
    while True:
        input_1 = input().strip().lower()
        if input_1 in ['exit', 'вихід']:
            break

        operation = input().strip().lower()
        if operation in ['exit', 'вихід']:
            break

        input_2 = input().strip().lower()
        if input_2 in ['exit', 'вихід']:
            break

        try:
            num1 = float(input_1)
            num2 = float(input_2)
        except ValueError:
            continue

        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        elif operation == '/':
            if num2 == 0:
                continue
            result = num1 / num2
        else:
            continue

        print(result)