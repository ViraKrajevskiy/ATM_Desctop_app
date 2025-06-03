import json
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button


class LanguageSelector(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.lang_map = {
            "English": "en",
            "Русский": "ru",
            "O‘zbekcha": "uz"
        }

        self.label = Label(text="Выберите язык / Choose language / Tilni tanlang", font_size=24)
        self.add_widget(self.label)

        for lang_name in self.lang_map:
            btn = Button(text=lang_name, font_size=20, size_hint=(1, 0.2))
            btn.bind(on_press=self.set_language)
            self.add_widget(btn)

    def set_language(self, instance):
        selected_lang = self.lang_map[instance.text]
        self.load_translations(selected_lang)

    def load_translations(self, lang_code):
        current_dir = os.path.dirname(__file__)
        # Путь к файлу translation.json в другой папке (Backend/functions/translate)
        file_path = os.path.join(current_dir, "Backend", "functions","main_menu", "translation.json")
        file_path = os.path.abspath(file_path)

        with open(file_path, "r", encoding="utf-8") as f:
            translations = json.load(f)

        current_language = translations.get(lang_code, {})
        print(f"Выбран язык: {lang_code}")
        print("Переводы загружены:", current_language)

        # TODO: Переход к следующему окну/функции здесь
        self.label.text = f"Язык выбран: {lang_code}"


class LanguageApp(App):
    def build(self):
        return LanguageSelector()


if __name__ == "__main__":
    LanguageApp().run()
