import json

data = {
    "name": "John",
    "age": 20,
    "is_student": True,
    "skills": ["programming", "drawing", "cooking"],
    "pet": None,
}

print('------------------- Основы записи и чтения -----------------------')

json_str = json.dumps(data)
print(f'Строка json: {json_str}')

renewed_data = json.loads(json_str)
print(f'Объект python: {renewed_data}')
# Данные до и после совпадают

print("------------ Преобразования русского текста --------------")

rus_data = "Некоторый русский текст"
print(f"Без спец атрибута: {json.dumps(rus_data)}")
print(f"С спец атрибутом: {json.dumps(rus_data, ensure_ascii=False)}")
# Благодаря специальному атрибуту

print('--------------------- Работа с файлами -------------------------')

# Lesson -- office
monday_schedule = {
    'Математика': 30,
    'Русский': 25,
    'Физика': 27
}

print("Попытка записать в файл...")

try:
    with open('scratch/test_json.json', 'w', encoding='utf-8') as f:
            json.dump(monday_schedule, f, ensure_ascii=False, indent=2)
except Exception:
    print('Запись в файл не удалась')
else:
    print('Информация успешно записана в файл')

print('Попытка прочитать файл...')

try:
    with open('scratch/test_json.json', 'r', encoding='utf-8') as f:
            print(json.load(f))
except Exception:
    print('Не удалось прочитать файл')

print('--------------------- Возможно ли преобразовать в json множество? -----------------------')

try:
    print(json.dumps({1, 2, 3}))
except TypeError:
    print('Не удалось преобразовать множество в строку json')
# set нельзя поскольку json так устроен вот и всё. Что тут объяснять ☻