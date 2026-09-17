import json


class Note:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

    def __str__(self):
        return f"{self.name} -- {self.content}"

    def __repr__(self):
        return f"Note(name={self.name!r}, content={self.content!r})"

    def __eq__(self, other):
        if not isinstance(other, Note):
            return NotImplemented
        return self.name == other.name and self.content == other.content

    def edit(self, new_content: str) -> None:
        self.content = new_content

    def to_dict(self) -> dict[str, str]:
        return {"name": self.name, "content": self.content}


class Notebook:
    def __init__(self):
        self._notes: dict[int, Note] = {}
        self._next_id: int = 1

    def __len__(self) -> int:
        return len(self._notes)

    def add(self, name: str, content: str) -> int:
        if not name.strip():
            raise ValueError("Пустое имя недопустимо")

        note = Note(name, content)
        note_id: int = self._next_id

        self._notes[note_id] = note
        self._next_id += 1

        return note_id

    def find_by_id(self, target_id: int) -> Note | None:
        return self._notes.get(target_id)

    def delete(self, note_id: int) -> bool:
        if note_id not in self._notes:
            return False

        del self._notes[note_id]
        return True

    def all(self) -> list[tuple[int, Note]]:
        return [(note_id, note) for note_id, note in self._notes.items()]

    def find_by_name(self, term: str) -> list[tuple[int, Note]]:
        if not term:
            return list(self._notes.items())

        return [
            (note_id, note)
            for note_id, note in self._notes.items()
            if term.lower() in note.name.lower()
        ]

    def save(self, file):
        file.parent.mkdir(parents=True, exist_ok=True)
        notes_to_json = [
            {"id": note_id, **note.to_dict()} for note_id, note in self._notes.items()
        ]

        with file.open("w", encoding="utf-8") as f:
            json.dump(notes_to_json, f, ensure_ascii=False, indent=2)

    def load(self, file):
        if not file.exists():
            return

        with file.open("r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise TypeError(f"Ожидался список, получен {type(data).__name__}")

        self._notes = {note["id"]: Note(note["name"], note["content"]) for note in data}

        self._next_id = max(self._notes.keys(), default=0) + 1


if __name__ == "__main__":
    test_note = Note("Имя", "Контент")
    print(test_note)
    test_note.edit("Новый контент")
    print(test_note)
