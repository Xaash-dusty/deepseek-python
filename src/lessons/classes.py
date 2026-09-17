class Note:
    count = 0

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.done = False

        Note.count += 1

    def __str__(self):
        return f"[{'x' if self.done else ' '}] {self.title} - {self.text}"

    def __repr__(self):
        return f"Note(title={self.title!r}, done={self.done!r})"

    def __eq__(self, other):
        return self.title == other.title and self.text == other.text

    def change_status(self):
        self.done = not self.done

    def rename(self, new_title):
        self.title = new_title

first_note = Note("Классы", "Изучить классы python")
first_note.change_status()
first_note.rename("ООП")

second_note = Note("Футбол", "Сыграть в футбол во дворе в 17:00")
third_note = Note("Готовка", "Научиться готовить макароны по-флотски")
second_note_copy = Note("Футбол", "Сыграть в футбол во дворе в 17:00")

print(first_note)
print(second_note == second_note_copy)
print(repr(third_note))