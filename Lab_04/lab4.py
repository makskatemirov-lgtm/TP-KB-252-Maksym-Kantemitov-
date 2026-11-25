# Reverse Polish Notation (shunting-yard algorithm) and expression evaluation
# Example: 3 + 4 * 2 / (1 - 5) ^ 2  ->  3 4 2 * 1 5 - 2 ^ / +  ->  3.5

# operator: (priority, right associative)
OPERATORS = {
    "+": (1, False),
    "-": (1, False),
    "*": (2, False),
    "/": (2, False),
    "u-": (3, True),   # unary minus
    "^": (4, True),
}


def tokenize(expression):
    """Split the expression into numbers, operators and brackets.

    Unary minus (at the start, after an operator or after '(') is marked 'u-'.
    """
    tokens = []
    i = 0
    n = len(expression)
    while i < n:
        ch = expression[i]
        if ch.isspace():
            i += 1
        elif ch.isdigit() or ch == ".":
            start = i
            while i < n and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            number = expression[start:i]
            try:
                float(number)
            except ValueError:
                raise ValueError(f"Wrong number: {number}")
            tokens.append(number)
        elif ch in "+-*/^()":
            if ch == "-" and (not tokens or tokens[-1] in OPERATORS or tokens[-1] == "("):
                tokens.append("u-")
            elif ch == "+" and (not tokens or tokens[-1] in OPERATORS or tokens[-1] == "("):
                pass  # unary plus does nothing
            else:
                tokens.append(ch)
            i += 1
        else:
            raise ValueError(f"Unknown symbol: {ch}")
    return tokens


def to_rpn(expression):
    """Convert infix expression to a list of RPN tokens."""
    output = []
    stack = []
    for token in tokenize(expression):
        if token in OPERATORS:
            priority, right = OPERATORS[token]
            if token != "u-":  # prefix operator never pops anything
                while stack and stack[-1] in OPERATORS:
                    top_priority = OPERATORS[stack[-1]][0]
                    if top_priority > priority or (top_priority == priority and not right):
                        output.append(stack.pop())
                    else:
                        break
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            if not stack:
                raise ValueError("Brackets are not matched")
            stack.pop()  # remove "("
        else:
            output.append(token)
    while stack:
        top = stack.pop()
        if top == "(":
            raise ValueError("Brackets are not matched")
        output.append(top)
    return output


def calculate_rpn(rpn):
    """Evaluate a list of RPN tokens and return the result."""
    stack = []
    for token in rpn:
        if token == "u-":
            if not stack:
                raise ValueError("Wrong expression")
            stack.append(-stack.pop())
        elif token in OPERATORS:
            if len(stack) < 2:
                raise ValueError("Wrong expression")
            b = stack.pop()
            a = stack.pop()
            if token == "+":
                stack.append(a + b)
            elif token == "-":
                stack.append(a - b)
            elif token == "*":
                stack.append(a * b)
            elif token == "/":
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            elif token == "^":
                try:
                    value = a ** b
                except OverflowError:
                    raise ValueError("Result is too big")
                if isinstance(value, complex):
                    raise ValueError("Result is not a real number")
                stack.append(value)
        else:
            stack.append(float(token))
    if len(stack) != 1:
        raise ValueError("Wrong expression")
    return stack[0]


def calculate(expression):
    """Full pipeline: infix string -> RPN -> result."""
    return calculate_rpn(to_rpn(expression))


def format_number(value):
    """3.0 -> '3', 3.5 -> '3.5'."""
    if value == int(value):
        return str(int(value))
    return str(value)


def main():
    while True:
        expression = input("Please enter expression (empty line to exit): ").strip()
        if not expression:
            print("Exit()")
            break
        try:
            rpn = to_rpn(expression)
            print("RPN: " + " ".join(rpn))
            print("Result: " + format_number(calculate_rpn(rpn)))
        except (ValueError, ZeroDivisionError) as error:
            print(f"Error: {error}")


if __name__ == "__main__":
    main()
