import pytest

import lab2
from lab2 import (
    find_index_by_name,
    find_insert_position,
    insert_student,
    is_valid_email,
    is_valid_phone,
    load_students,
    remove_student,
    replace_student,
    save_students,
)


def make(name, phone="0631234567", group="kb-242"):
    return {"name": name, "phone": phone,
            "email": f"{name.lower()}@gmail.com", "group": group}


@pytest.fixture(autouse=True)
def base_list():
    """Every test starts with the same sorted list."""
    lab2.students[:] = [make("Bob"), make("Emma"), make("Jon"), make("Zak")]
    yield
    lab2.students[:] = []


def names():
    return [s["name"] for s in lab2.students]


# ------------------------------------------------------------ validation

def test_phone_valid():
    assert is_valid_phone("0631234567")


def test_phone_wrong_length():
    assert not is_valid_phone("063123456")
    assert not is_valid_phone("06312345678")


def test_phone_not_digits():
    assert not is_valid_phone("063123456a")
    assert not is_valid_phone("+380631234")
    assert not is_valid_phone("")


def test_email_valid():
    assert is_valid_email("jon@gmail.com")
    assert is_valid_email("jon.smith+tag@mail.ua")


def test_email_invalid():
    assert not is_valid_email("jon")
    assert not is_valid_email("jon@gmail")
    assert not is_valid_email("@gmail.com")
    assert not is_valid_email("jon@@gmail.com")


# ---------------------------------------------------------------- search

def test_find_index_existing():
    assert find_index_by_name("Bob") == 0
    assert find_index_by_name("Zak") == 3


def test_find_index_case_insensitive():
    assert find_index_by_name("eMmA") == 1


def test_find_index_missing():
    assert find_index_by_name("Nobody") == -1


def test_insert_position_begin_middle_end():
    assert find_insert_position("Adam") == 0
    assert find_insert_position("Hanna") == 2
    assert find_insert_position("Zoe") == 4


def test_insert_position_case_insensitive():
    assert find_insert_position("BOBBY") == 1


# ------------------------------------------------------------------ add

def test_insert_keeps_sorted():
    insert_student(make("Hanna"))
    insert_student(make("Adam"))
    insert_student(make("Zoe"))
    assert names() == ["Adam", "Bob", "Emma", "Hanna", "Jon", "Zak", "Zoe"]


def test_insert_into_empty_list():
    lab2.students.clear()
    assert insert_student(make("Bob")) == 0
    assert names() == ["Bob"]


# --------------------------------------------------------------- delete

def test_remove_existing():
    assert remove_student("Emma") == 1
    assert names() == ["Bob", "Jon", "Zak"]


def test_remove_missing():
    assert remove_student("Nobody") == -1
    assert len(lab2.students) == 4


# --------------------------------------------------------------- update

def test_replace_existing_same_name():
    new_item = make("Jon", phone="0990000000")
    assert replace_student("Jon", new_item)
    assert lab2.students[2]["phone"] == "0990000000"
    assert len(lab2.students) == 4


def test_replace_existing_new_name_keeps_sorted():
    assert replace_student("Bob", make("Yan"))
    assert names() == ["Emma", "Jon", "Yan", "Zak"]


def test_replace_missing():
    assert not replace_student("Nobody", make("Yan"))
    assert names() == ["Bob", "Emma", "Jon", "Zak"]


# ----------------------------------------------------------------- files

def test_load_students(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text(
        "name,phone,email,group\n"
        "Zak,0631234570,zak@gmail.com,kb-242\n"
        "bob,0631234567,bob@gmail.com,kb-241\n",
        encoding="utf-8",
    )
    result = load_students(str(path))
    assert [s["name"] for s in result] == ["bob", "Zak"]  # sorted
    assert result[0] == {"name": "bob", "phone": "0631234567",
                         "email": "bob@gmail.com", "group": "kb-241"}


def test_load_keeps_leading_zero_in_phone(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone,email,group\nA,0631234567,a@b.com,g\n")
    assert load_students(str(path))[0]["phone"] == "0631234567"


def test_load_empty_file_with_header(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone,email,group\n")
    assert load_students(str(path)) == []


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_students(str(tmp_path / "missing.csv"))


def test_load_missing_column(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone\nBob,0631234567\n")
    with pytest.raises(KeyError):
        load_students(str(path))


def test_save_students_writes_header_and_rows(tmp_path):
    path = tmp_path / "out.csv"
    save_students(str(path), lab2.students)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "name,phone,email,group"
    assert lines[1] == "Bob,0631234567,bob@gmail.com,kb-242"
    assert len(lines) == 5


def test_save_then_load_roundtrip(tmp_path):
    path = str(tmp_path / "round.csv")
    save_students(path, lab2.students)
    assert load_students(path) == lab2.students


def test_roundtrip_with_comma_in_field(tmp_path):
    path = str(tmp_path / "comma.csv")
    items = [{"name": "Smith, John", "phone": "0631234567",
              "email": "j@gmail.com", "group": "kb-242"}]
    save_students(path, items)
    assert load_students(path) == items


# ------------------------------------------------------- input functions

def test_input_phone_retries_until_valid(monkeypatch, capsys):
    answers = iter(["abc", "123", "0631234567"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab2.input_phone("phone: ") == "0631234567"
    assert "10 digits" in capsys.readouterr().out


def test_input_email_retries_until_valid(monkeypatch):
    answers = iter(["bad", "ok@gmail.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab2.input_email("email: ") == "ok@gmail.com"


def test_input_non_empty_retries(monkeypatch):
    answers = iter(["", "   ", " Bob "])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab2.input_non_empty("name: ") == "Bob"


def test_add_new_element(monkeypatch):
    answers = iter(["Anna", "0501112233", "anna@gmail.com", "kb-242"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    lab2.add_new_element()
    assert names() == ["Anna", "Bob", "Emma", "Jon", "Zak"]


def test_delete_element(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "jon")
    lab2.delete_element()
    assert names() == ["Bob", "Emma", "Zak"]


def test_update_element(monkeypatch):
    answers = iter(["Bob", "Yan", "0501112233", "yan@gmail.com", "kb-241"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    lab2.update_element()
    assert names() == ["Emma", "Jon", "Yan", "Zak"]
    assert lab2.students[2]["group"] == "kb-241"


# ------------------------------------------------------------- main loop

def test_main_loads_and_saves_on_exit(tmp_path, monkeypatch):
    path = tmp_path / "book.csv"
    save_students(str(path), lab2.students)
    answers = iter(["d", "Bob", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(lab2, "argv", ["lab2.py", str(path)])
    lab2.main()
    assert [s["name"] for s in load_students(str(path))] == ["Emma", "Jon", "Zak"]


def test_main_without_argument(monkeypatch, capsys):
    monkeypatch.setattr(lab2, "argv", ["lab2.py"])
    lab2.main()
    assert "Usage" in capsys.readouterr().out


def test_main_file_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(lab2, "argv", ["lab2.py", str(tmp_path / "no.csv")])
    lab2.main()
    assert "was not found" in capsys.readouterr().out
