from notes import (
    DATA_PATH,
    add_note,
    delete_note,
    edit_note,
    find_by_id,
    find_by_name,
    load_notes,
)


def show_note(note: dict) -> None:
    for key, value in note.items():
        print(f"{key}: {value}")
    print("_" * 50)


def main():
    print("CLI-заметки. Введите 'help' для списка команд.")
    print("Введите 'quit' для выхода.")

    notes = load_notes(DATA_PATH)

    while True:
        try:
            command = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        match cmd:
            case "quit":
                break
            case "help":
                print("Команды: add, list, show, find, edit, delete, quit")
            case "list":
                if not notes:
                    print("Заметок нет")
                    continue
                for note in notes:
                    print(f"{note['id']}: {note['name']}")
            case "show":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                try:
                    note_id = int(args[0])
                except ValueError:
                    print("Вы ввели некорректный id, нужно натуральное число")
                    continue

                note = find_by_id(notes, note_id)

                if note is None:
                    print(f"Заметка с id {note_id} не найдена")
                    continue

                show_note(note)
            case "add":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                name = " ".join(args)
                print(f"Имя: {name}")
                content = input("Контент: ")

                try:
                    note_id = add_note(notes, name, content, DATA_PATH)
                    print(f"Заметка успешно добавлена, id: {note_id}")
                except ValueError as e:
                    print(f"Ошибка: {e}")
            case "find":
                full = "--more" in args
                if full:
                    args = args[:args.index("--more")]
                search_term = " ".join(args)

                result = find_by_name(notes, search_term)

                if not result:
                    print("Заметки не найдены")
                    continue

                if full:
                    for note in result:
                        show_note(note)
                else:
                    for note in result:
                        print(f"{note['id']}: {note['name']}")
            case "delete":
                if not args:
                    print("Вы не передали аргументы")
                    continue

                try:
                    note_id = int(args[0])
                except ValueError:
                    print("Вы ввели некорректный id, нужно натуральное число")
                    continue

                is_deleted = delete_note(notes, note_id, DATA_PATH)

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

                new_content = input("Новое содержимое заметки: ")
                is_edited = edit_note(notes, note_id, new_content, DATA_PATH)

                if is_edited:
                    print(f"Содержимое заметки успешно обновлено, id: {note_id}")
                else:
                    print(f"Заметка с id {note_id} не найдена")
            case _:
                print(f"Неизвестная команда: {cmd}")

    print("\nВыход")


if __name__ == "__main__":
    main()
