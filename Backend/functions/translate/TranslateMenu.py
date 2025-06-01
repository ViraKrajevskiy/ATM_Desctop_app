# with open("translation.json", "r", encoding="utf-8") as f:
#     translations = json.load(f)
import os
import json

# Абсолютный путь к файлу translation.json
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "translation.json")

with open(file_path, "r", encoding="utf-8") as f:
    translations = json.load(f)

current_language = None


def select_language():
    lang_map = {
        1: "en",
        2: "ru",
        3: "uz"
    }

    while True:
        print("Выберите язык:")
        print("1 - English")
        print("2 - Русский")
        print("3 - O‘zbekcha")

        user_input = input("Введите число 1/2/3: ").strip()

        if not user_input.isdigit():
            print("Ошибка: нужно ввести число от 1 до 3.\n1 dan 3 gacha bolgan sonni kiriting.\nEnter a number 1 to 3.")
            continue

        lang_code = int(user_input)

        if lang_code not in lang_map:
            print("Неверный код выберите от 1 до 3.")
            return select_language()

        return lang_map[lang_code]