import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # ../src/projects/notes
DATA_PATH = BASE_DIR.parent.parent.parent / "data" / "notes.json"


def load_notes(file) -> list[dict]:
    if not file.exists():
        return []
    # Если файл битый ошибка поднимается обрабатывается в main
    with file.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise TypeError(f"Ожидался список, получен {type(data).__name__}")

    return data


def save_notes(file, notes: list[dict]) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)

    with file.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)


def add_note(notes: list[dict], name: str, content: str, file) -> int:
    if not name.strip():
        raise ValueError("Пустое имя недопустимо")

    note_id: int = max((n["id"] for n in notes), default=0) + 1

    notes.append({"id": note_id, "name": name, "content": content})
    save_notes(file, notes)

    return note_id


def find_by_id(notes: list[dict], note_id: int) -> dict | None:
    return next((n for n in notes if n["id"] == note_id), None)


def find_by_name(notes: list[dict], searching_term: str) -> list[dict]:
    # Если поисковый запрос пуст возвращается все
    if not searching_term.strip():
        return notes

    return [n for n in notes if searching_term.lower() in n["name"].lower()]


def delete_note(notes: list[dict], note_id: int, file) -> bool:
    target = find_by_id(notes, note_id)

    if target is None:
        return False

    # Зачем искать индекс если удаление словаря происходит по ссылке и у нас есть эта ссылка и дубликатов быть не может
    notes.remove(target)
    save_notes(file, notes)
    return True


def edit_note(notes: list[dict], note_id: int, new_content: str, file) -> bool:
    note = find_by_id(notes, note_id)
    if note is None:
        return False

    note["content"] = new_content
    save_notes(file, notes)
    return True


