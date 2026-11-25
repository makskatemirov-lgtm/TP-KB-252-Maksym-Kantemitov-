import pytest

import lab3
from student import Student
from student_list import StudentList
from utils import CsvStorage


def make(name, phone="0631234567", group="kb-242"):
    return Student(name, phone, f"{name.lower()}@gmail.com", group)


@pytest.fixture
def students():
    return StudentList([make("Zak"), make("Bob"), make("Jon"), make("Emma")])


# ---------------------------------------------------------------- Student

def test_student_attributes():
    s = Student("Jon", "0631234567", "jon@gmail.com", "kb-242")
    assert (s.name, s.phone, s.email, s.group) == \
        ("Jon", "0631234567", "jon@gmail.com", "kb-242")


def test_student_str():
    assert str(make("Bob")) == (
        "Student name is Bob,  Phone is 0631234567,  "
        "Email is bob@gmail.com,  Group is kb-242")


def test_student_equality():
    assert make("Bob") == make("Bob")
    assert make("Bob") != make("Jon")
    assert make("Bob") != "Bob"


def test_student_dict_roundtrip():
    s = make("Bob")
    assert Student.from_dict(s.to_dict()) == s


def test_phone_valid():
    assert Student.is_valid_phone("0631234567")


def test_phone_invalid():
    assert not Student.is_valid_phone("063123456")
    assert not Student.is_valid_phone("06312345678")
    assert not Student.is_valid_phone("063123456a")
    assert not Student.is_valid_phone("")


def test_email_valid():
    assert Student.is_valid_email("jon@gmail.com")
    assert Student.is_valid_email("jon.smith+tag@mail.ua")


def test_email_invalid():
    assert not Student.is_valid_email("jon")
    assert not Student.is_valid_email("jon@gmail")
    assert not Student.is_valid_email("@gmail.com")
    assert not Student.is_valid_email("jon@@gmail.com")


# ------------------------------------------------------------ StudentList

def test_list_is_sorted_on_creation(students):
    assert students.names() == ["Bob", "Emma", "Jon", "Zak"]


def test_list_contains_student_objects(students):
    assert all(isinstance(s, Student) for s in students)


def test_empty_list():
    assert len(StudentList()) == 0


def test_len_and_getitem(students):
    assert len(students) == 4
    assert students[0].name == "Bob"


def test_find_index(students):
    assert students.find_index("Bob") == 0
    assert students.find_index("eMmA") == 1
    assert students.find_index("Nobody") == -1


def test_insert_position(students):
    assert students.find_insert_position("Adam") == 0
    assert students.find_insert_position("Hanna") == 2
    assert students.find_insert_position("Zoe") == 4
    assert students.find_insert_position("BOBBY") == 1


def test_add_keeps_sorted(students):
    students.add(make("Hanna"))
    students.add(make("Adam"))
    students.add(make("Zoe"))
    assert students.names() == ["Adam", "Bob", "Emma", "Hanna", "Jon", "Zak", "Zoe"]


def test_add_returns_position(students):
    assert students.add(make("Hanna")) == 2


def test_delete_existing(students):
    assert students.delete("Emma") == 1
    assert students.names() == ["Bob", "Jon", "Zak"]


def test_delete_missing(students):
    assert students.delete("Nobody") == -1
    assert len(students) == 4


def test_update_same_name(students):
    assert students.update("Jon", make("Jon", phone="0990000000"))
    assert students[2].phone == "0990000000"
    assert len(students) == 4


def test_update_new_name_keeps_sorted(students):
    assert students.update("Bob", make("Yan"))
    assert students.names() == ["Emma", "Jon", "Yan", "Zak"]


def test_update_missing(students):
    assert not students.update("Nobody", make("Yan"))
    assert students.names() == ["Bob", "Emma", "Jon", "Zak"]


def test_print_all(students, capsys):
    students.print_all()
    out = capsys.readouterr().out.splitlines()
    assert len(out) == 4
    assert out[0] == str(make("Bob"))


def test_print_empty(capsys):
    StudentList().print_all()
    assert capsys.readouterr().out.strip() == "List is empty"


# ------------------------------------------------------------ CsvStorage

def test_load(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text(
        "name,phone,email,group\n"
        "Zak,0631234570,zak@gmail.com,kb-242\n"
        "bob,0631234567,bob@gmail.com,kb-241\n", encoding="utf-8")
    result = CsvStorage(str(path)).load()
    assert isinstance(result, StudentList)
    assert result.names() == ["bob", "Zak"]
    assert result[0] == Student("bob", "0631234567", "bob@gmail.com", "kb-241")


def test_load_keeps_leading_zero(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone,email,group\nA,0631234567,a@b.com,g\n")
    assert CsvStorage(str(path)).load()[0].phone == "0631234567"


def test_load_empty_file_with_header(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone,email,group\n")
    assert len(CsvStorage(str(path)).load()) == 0


def test_load_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        CsvStorage(str(tmp_path / "missing.csv")).load()


def test_load_missing_column(tmp_path):
    path = tmp_path / "in.csv"
    path.write_text("name,phone\nBob,0631234567\n")
    with pytest.raises(KeyError):
        CsvStorage(str(path)).load()


def test_save_writes_header_and_rows(tmp_path, students):
    path = tmp_path / "out.csv"
    CsvStorage(str(path)).save(students)
    lines = path.read_text(encoding="utf-8").splitlines()
    assert lines[0] == "name,phone,email,group"
    assert lines[1] == "Bob,0631234567,bob@gmail.com,kb-242"
    assert len(lines) == 5


def test_save_load_roundtrip(tmp_path, students):
    storage = CsvStorage(str(tmp_path / "r.csv"))
    storage.save(students)
    assert list(storage.load()) == list(students)


def test_roundtrip_comma_in_field(tmp_path):
    storage = CsvStorage(str(tmp_path / "c.csv"))
    original = StudentList([Student("Smith, John", "0631234567", "j@gmail.com", "kb-242")])
    storage.save(original)
    assert list(storage.load()) == list(original)


# ------------------------------------------------------- input / main

def test_input_phone_retries(monkeypatch, capsys):
    answers = iter(["abc", "123", "0631234567"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab3.input_phone("phone: ") == "0631234567"
    assert "10 digits" in capsys.readouterr().out


def test_input_email_retries(monkeypatch):
    answers = iter(["bad", "ok@gmail.com"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab3.input_email("email: ") == "ok@gmail.com"


def test_input_non_empty_retries(monkeypatch):
    answers = iter(["", "   ", " Bob "])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab3.input_non_empty("name: ") == "Bob"


def test_read_student(monkeypatch):
    answers = iter(["Anna", "0501112233", "anna@gmail.com", "kb-242"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    assert lab3.read_student() == Student("Anna", "0501112233", "anna@gmail.com", "kb-242")


def test_add_new_element(monkeypatch, students):
    answers = iter(["Anna", "0501112233", "anna@gmail.com", "kb-242"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    lab3.add_new_element(students)
    assert students.names() == ["Anna", "Bob", "Emma", "Jon", "Zak"]


def test_delete_element(monkeypatch, students):
    monkeypatch.setattr("builtins.input", lambda _: "jon")
    lab3.delete_element(students)
    assert students.names() == ["Bob", "Emma", "Zak"]


def test_delete_element_missing(monkeypatch, students, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "nobody")
    lab3.delete_element(students)
    assert "not found" in capsys.readouterr().out
    assert len(students) == 4


def test_update_element(monkeypatch, students):
    answers = iter(["Bob", "Yan", "0501112233", "yan@gmail.com", "kb-241"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    lab3.update_element(students)
    assert students.names() == ["Emma", "Jon", "Yan", "Zak"]
    assert students[2].group == "kb-241"


def test_main_loads_and_saves_on_exit(tmp_path, monkeypatch, students):
    path = tmp_path / "book.csv"
    CsvStorage(str(path)).save(students)
    answers = iter(["d", "Bob", "x"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))
    monkeypatch.setattr(lab3, "argv", ["lab3.py", str(path)])
    lab3.main()
    assert CsvStorage(str(path)).load().names() == ["Emma", "Jon", "Zak"]


def test_main_without_argument(monkeypatch, capsys):
    monkeypatch.setattr(lab3, "argv", ["lab3.py"])
    lab3.main()
    assert "Usage" in capsys.readouterr().out


def test_main_file_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(lab3, "argv", ["lab3.py", str(tmp_path / "no.csv")])
    lab3.main()
    assert "was not found" in capsys.readouterr().out
