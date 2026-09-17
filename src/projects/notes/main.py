import json
from pathlib import Path

from models import Note, Notebook

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR.parent.parent.parent / "data" / "notes.json"


def show_note(note_id: int, note: Note) -> None:
    print(f"id: {note_id}")
    print(f"name: {note.name}")
    print(f"content: {note.content}")
    print("_" * 50)


def main():
    print("CLI-заметки. Введите 'help' для списка команд.")
    print("Введите 'quit' для выхода.")

    try:
        nb = Notebook()
        nb.load(DATA_PATH)
    except TypeError as e:
        print(e)
        return
    except json.JSONDecodeError:
        print("Файл битый")
        return
    while True:
        try:
            command = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:]

        match cmd:
            case "quit":
                break
            case "help":
                print("Команды: add, list, show, find, edit, delete, quit")
            case "list":
                if not nb:
                    print("Заметок нет")
                    continue
                for note_id, note in nb.all():
                    print(f"{note_id}: {note.name}")
            case "show":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                try:
                    note_id = int(args[0])
                except ValueError:
                    print("Вы ввели некорректный id, нужно натуральное число")
                    continue

                note = nb.find_by_id(note_id)

                if note is None:
                    print(f"Заметка с id {note_id} не найдена")
                    continue

                show_note(note_id, note)
            case "add":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                name = " ".join(args)

                print(f"Имя: {name}")
                content = input("Контент: ")

                try:
                    note_id = nb.add(name, content)
                    nb.save(DATA_PATH)
                    print(f"Заметка успешно добавлена, id: {note_id}")
                except ValueError as e:
                    print(e)
            case "find":
                full = "--more" in args
                if full:
                    args = args[: args.index("--more")]
                search_term = " ".join(args)

                result = nb.find_by_name(search_term)

                if not result:
                    print("Заметки не найдены")
                    continue

                if full:
                    for note_id, note in result:
                        show_note(note_id, note)
                else:
                    for note_id, note in result:
                        print(f"{note_id}: {note.name}")
            case "delete":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                try:
                    note_id = int(args[0])
                except ValueError:
                    print("Вы ввели некорректный id, нужно натуральное число")
                    continue

                is_deleted = nb.delete(note_id)
                nb.save(DATA_PATH)

                if is_deleted:
                    print("Заметка успешно удалена")
                else:
                    print("Заметки с таким id не существует")
            case "edit":
                if len(args) != 1:
                    print("edit принимает один аргумент: id")
                    continue
                try:
                    note_id = int(args[0])
                except ValueError:
                    print("Вы ввели некорректный id, нужно натуральное число")
                    continue

                note = nb.find_by_id(note_id)
                if note is None:
                    print(f"Заметка с id {note_id} не найдена")
                    continue

                new_content = input("Новое содержимое заметки: ")
                note.edit(new_content)
                nb.save(DATA_PATH)
                print(f"Содержимое заметки успешно обновлено, id: {note_id}")
            case _:
                print(f"Неизвестная команда: {cmd}\nНапишите `help` чтобы получить инструкции")

    print("\nВыход")


if __name__ == "__main__":
    main()
