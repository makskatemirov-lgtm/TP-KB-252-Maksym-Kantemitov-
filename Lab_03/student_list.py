from student import Student


class StudentList:
    """Group list. Stores Student objects sorted by name (case-insensitive)."""

    def __init__(self, students=None):
        self._items = []
        for student in students or []:
            self.add(student)

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __getitem__(self, index):
        return self._items[index]

    def names(self):
        return [s.name for s in self._items]

    def find_insert_position(self, name):
        """Find the position that keeps the list sorted by name."""
        position = 0
        for item in self._items:
            if name.lower() > item.name.lower():
                position += 1
            else:
                break
        return position

    def find_index(self, name):
        """Return index of the first student with the given name or -1."""
        for i, item in enumerate(self._items):
            if item.name.lower() == name.lower():
                return i
        return -1

    def add(self, student):
        """Insert student keeping the list sorted. Return the position."""
        position = self.find_insert_position(student.name)
        self._items.insert(position, student)
        return position

    def delete(self, name):
        """Delete the first student with the given name. Return index or -1."""
        index = self.find_index(name)
        if index != -1:
            del self._items[index]
        return index

    def update(self, name, new_student):
        """Replace the student with the given name. Return True if found."""
        if self.delete(name) == -1:
            return False
        self.add(new_student)
        return True

    def print_all(self):
        if not self._items:
            print("List is empty")
            return
        for student in self._items:
            print(student)
