import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class Student:
    """One student of the group."""

    def __init__(self, name, phone, email, group):
        self.name = name
        self.phone = phone
        self.email = email
        self.group = group

    @staticmethod
    def is_valid_phone(value):
        """Phone is valid if it contains exactly 10 digits."""
        return value.isdigit() and len(value) == 10

    @staticmethod
    def is_valid_email(value):
        """Email is valid if it matches EMAIL_PATTERN."""
        return EMAIL_PATTERN.match(value) is not None

    def to_dict(self):
        return {"name": self.name, "phone": self.phone,
                "email": self.email, "group": self.group}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["phone"], data["email"], data["group"])

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.to_dict() == other.to_dict()

    def __str__(self):
        return (f"Student name is {self.name},  Phone is {self.phone},  "
                f"Email is {self.email},  Group is {self.group}")

    def __repr__(self):
        return f"Student({self.name!r}, {self.phone!r}, {self.email!r}, {self.group!r})"
