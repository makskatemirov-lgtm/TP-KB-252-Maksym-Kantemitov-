import pytest

import lab4
from lab4 import calculate, calculate_rpn, format_number, to_rpn, tokenize


def rpn(expression):
    return " ".join(to_rpn(expression))


# -------------------------------------------------------------- tokenize

def test_tokenize_simple():
    assert tokenize("3+4") == ["3", "+", "4"]


def test_tokenize_spaces_and_decimals():
    assert tokenize(" 1.5 *  2 ") == ["1.5", "*", "2"]


def test_tokenize_unary_minus():
    assert tokenize("-3") == ["u-", "3"]
    assert tokenize("2*-3") == ["2", "*", "u-", "3"]
    assert tokenize("(-3)") == ["(", "u-", "3", ")"]
    assert tokenize("5-3") == ["5", "-", "3"]


def test_tokenize_unknown_symbol():
    with pytest.raises(ValueError):
        tokenize("3 + a")


def test_tokenize_wrong_number():
    with pytest.raises(ValueError):
        tokenize("1.2.3 + 4")


# ------------------------------------------------------------------- RPN

def test_rpn_example_from_task():
    assert rpn("3 + 4 * 2 / (1 - 5) ^ 2") == "3 4 2 * 1 5 - 2 ^ / +"


def test_rpn_priority():
    assert rpn("1 + 2 * 3") == "1 2 3 * +"
    assert rpn("1 * 2 + 3") == "1 2 * 3 +"


def test_rpn_left_associativity():
    assert rpn("8 - 3 - 2") == "8 3 - 2 -"
    assert rpn("8 / 4 / 2") == "8 4 / 2 /"


def test_rpn_power_right_associativity():
    assert rpn("2 ^ 3 ^ 2") == "2 3 2 ^ ^"


def test_rpn_brackets():
    assert rpn("(1 + 2) * 3") == "1 2 + 3 *"
    assert rpn("((1 + 2) * (3 + 4))") == "1 2 + 3 4 + *"


def test_rpn_single_number():
    assert rpn("42") == "42"


def test_rpn_unary_minus():
    assert rpn("-2 ^ 2") == "2 2 ^ u-"
    assert rpn("2 * -3") == "2 3 u- *"


def test_rpn_brackets_not_matched():
    for bad in ("(1 + 2", "1 + 2)", "((1)", ")("):
        with pytest.raises(ValueError):
            to_rpn(bad)


# ------------------------------------------------------------ evaluation

def test_calculate_example_from_task():
    assert calculate("3 + 4 * 2 / (1 - 5) ^ 2") == 3.5


@pytest.mark.parametrize("expression, expected", [
    ("1 + 2", 3),
    ("5 - 7", -2),
    ("6 * 7", 42),
    ("9 / 2", 4.5),
    ("2 ^ 10", 1024),
    ("2 ^ 3 ^ 2", 512),
    ("(1 + 2) * (3 + 4)", 21),
    ("10 - 4 - 3", 3),
    ("100 / 10 / 5", 2),
    ("1.5 + 2.5", 4),
    ("-5 + 3", -2),
    ("-2 ^ 2", -4),
    ("(-2) ^ 2", 4),
    ("2 * -3", -6),
    ("--3", 3),
    ("+5", 5),
    ("2 ^ 0.5 * 2 ^ 0.5", pytest.approx(2)),
    ("((((7))))", 7),
    ("2 + 3 * 4 - 5 / (1 + 1)", 11.5),
])
def test_calculate(expression, expected):
    assert calculate(expression) == expected


def test_division_by_zero():
    with pytest.raises(ZeroDivisionError):
        calculate("1 / 0")
    with pytest.raises(ZeroDivisionError):
        calculate("1 / (2 - 2)")


@pytest.mark.parametrize("bad", ["", "   ", "1 +", "* 2", "1 2", "1 + * 2", "()", "(1 + 2) 3"])
def test_wrong_expression(bad):
    with pytest.raises(ValueError):
        calculate(bad)


def test_negative_base_fractional_power():
    with pytest.raises(ValueError):
        calculate("(-8) ^ 0.5")


def test_too_big_result():
    with pytest.raises(ValueError):
        calculate("10.5 ^ 10000")


def test_calculate_rpn_directly():
    assert calculate_rpn(["3", "4", "2", "*", "1", "5", "-", "2", "^", "/", "+"]) == 3.5


# ---------------------------------------------------------------- output

def test_format_number():
    assert format_number(3.0) == "3"
    assert format_number(3.5) == "3.5"
    assert format_number(-4.0) == "-4"


def test_main(monkeypatch, capsys):
    answers = iter(["3 + 4 * 2 / (1 - 5) ^ 2", "1 / 0", "(1", ""])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    lab4.main()
    out = capsys.readouterr().out
    assert "RPN: 3 4 2 * 1 5 - 2 ^ / +" in out
    assert "Result: 3.5" in out
    assert "Error: Division by zero" in out
    assert "Error: Brackets are not matched" in out
    assert "Exit()" in out
