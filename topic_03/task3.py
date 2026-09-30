def test_dict_methods():
    student = {
        "name": "Олексій",
        "age": 20,
        "city": "Київ"
    }

    student.keys()
    student.values()
    student.items()

    student.update({"age": 21, "course": 3})
    del student["city"]
    student.clear()