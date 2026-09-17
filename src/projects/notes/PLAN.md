# Основная информация

**Название**: CLI-заметки (ООП)
**Суть**: Управление заметками через классы
**Основа**: переписываем проект этапа 1 на ООП
___
# Структура

### Хранение

***Файл***: `data/notes.json` (**путь от файла скрипта**)  
***Формат на диске***: не меняется — список словарей `{"id": int, "name": str, "content": str}`  
***Представление в памяти***: `dict[int, Note]`, где ключ — id, значение — объект `Note`
___
# Классы

### `Note` — одна заметка

**Файл**: `src/projects/notes/models.py`
**Поля**: `name: str`, `content: str` (id здесь **нет** — им владеет `Notebook`)

**Методы**:
- `__init__(self, name, content)` — создать заметку
- `__str__(self)` — читаемая строка для `print`
- `__repr__(self)` — для отладки
- `__eq__(self, other)` — сравнение по `name` и `content` (+ `isinstance`-проверка)
- `edit(self, new_content)` — заменить `content`
- `to_dict(self)` — `{"name": ..., "content": ...}` для сериализации

### `Notebook` — коллекция заметок

**Файл**: `src/projects/notes/models.py`
**Поля**: `_notes: dict[int, Note]`, `_next_id: int`

**Методы**:
- `__init__(self)` — пустой блокнот, `_next_id = 1`
- `add(self, name, content) -> int` — добавить, вернуть id
- `delete(self, note_id) -> bool` — удалить по id
- `find_by_id(self, note_id) -> Note | None`
- `find_by_name(self, term) -> list[tuple[int, Note]]` — частичный поиск, регистр не важен
- `all(self) -> list[tuple[int, Note]]`
- `save(self, path) -> None` — записать в JSON
- `load(self, path) -> None` — прочитать JSON, заполнить `_notes`, пересчитать `_next_id`

### `main.py` — CLI

**Файл**: `src/projects/notes/main.py`
**Задачи**: без изменений — ввод/вывод, команды, валидация ввода.  
**Отличие**: вместо вызова функций — вызовы методов (`nb.add(...)`, `nb.save(DATA_PATH)` и т.д.)
___
# Правила

- `id` присваивает **`Notebook`**. В `Note` его нет.
- `_next_id` — инстанс-атрибут. При `load` — `max(_notes.keys(), default=0) + 1`.
- `save`/`load` **не вызываются** внутри `add`/`delete`/`edit`. Их зовёт `main.py` явно после изменяющих команд (единственная ответственность).
- `save` сериализует: `[{"id": i, **n.to_dict()} for i, n in self._notes.items()]`.
- `load` десериализует: для каждого словаря создаёт `Note(d["name"], d["content"])`, кладёт по ключу `d["id"]`.
- Формат JSON и команды CLI — **без изменений**.
- `_name` — соглашение о приватности (Python не запрещает доступ, но снаружи не трогаем).
___
# Отложенные идеи

- Отдельный класс `NoteStorage` (если понадобится менять хранилище).
- `Note.from_dict()` через `@classmethod` (новая синтаксика, позже).
- Из старого плана: даты, CLI-аргументы, кастомные ошибки, очистка списка.