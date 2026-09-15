with open("scratch/test.txt", "w", encoding="utf-8") as f:
    f.writelines(["first\n", "second\n", "third\n"])

with open("scratch/test.txt", "r", encoding="utf-8") as f:
    content = f.read()
    print(content)
    print(len(content))
print("-------- Чтение построчно ---------")
with open("scratch/test.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.rstrip())
        print(
            f"Row line length: {len(line)};\nStriped line length: {len(line.rstrip())}"
        )

with open("scratch/test.txt", "a", encoding="utf-8") as f:
    f.write("четвертая\n")
print("--------------- Чтение после дозаписи -------------")
with open("scratch/test.txt", "r", encoding="utf-8") as f:
    print(f.read())

with open('scratch/test.txt', 'w', encoding='utf-8') as f:
    pass
print('---------- Попытка чтения после отчистки ---------------')
with open("scratch/test.txt", "r", encoding="utf-8") as f:
    print(f.read())

print('------------ Открытие несуществующего файла --------------')
try:
    with open('non-existing.txt', 'r', encoding='utf-8') as f:
        print(f.read())
except FileNotFoundError:
    print('Файл не существует')