from Backend.functions.Bank_worker_dashboard.main_func import *
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, RoundedRectangle
from Backend.functions.translate.TranslateMenu import translations


class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from Backend.functions.main_menu.front_main_menu import RoundedButton

        # Основной layout с фоном
        self.main_layout = BoxLayout(orientation='vertical')
        with self.main_layout.canvas.before:
            # Градиентный фон
            Color(0.2, 0.5, 0.7, 1)  # Темно-синий цвет
            self.bg = Rectangle(pos=self.main_layout.pos, size=Window.size)

        self.main_layout.bind(pos=self.update_bg, size=self.update_bg)

        # Контейнер с закругленными углами для контента
        content_container = BoxLayout(orientation='vertical', padding=20, spacing=20,
                                      size_hint=(0.9, 0.9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        with content_container.canvas.before:
            Color(1, 1, 1, 0.9)  # Полупрозрачный белый
            self.content_bg = RoundedRectangle(pos=content_container.pos,
                                               size=content_container.size,
                                               radius=[25])

        content_container.bind(pos=self.update_content_bg, size=self.update_content_bg)

        # Заголовок
        self.title_label = Label(
            text='About Us',
            font_size=24,
            bold=True,
            color=(0, 0, 0, 1)  # Черный цвет текста
        )

        # ScrollView для текста
        scroll = ScrollView()
        self.text_content = BoxLayout(orientation='vertical', size_hint_y=None)
        self.text_content.bind(minimum_height=self.text_content.setter('height'))

        self.info_label = Label(
            text='',
            font_size=18,
            size_hint_y=None,
            halign='left',
            valign='top',
            color=(0.1, 0.1, 0.1, 1),  # Темно-серый текст
            text_size=(Window.width * 0.8, None),
            padding=(10, 10)
        )
        self.info_label.bind(texture_size=self.info_label.setter('size'))
        self.text_content.add_widget(self.info_label)
        scroll.add_widget(self.text_content)

        # Кнопка возврата с закругленными углами
        btn_back = Button(
            text='Back to Menu',
            size_hint=(0.5, None),
            height=50,
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0, 0, 0, 0)  # Прозрачный фон для видимости rounded corners
        )

        # Добавляем закругленные углы к кнопке
        with btn_back.canvas.before:
            Color(0.2, 0.5, 0.8, 1)  # Синий цвет кнопки
            btn_back.rect = RoundedRectangle(
                pos=btn_back.pos,
                size=btn_back.size,
                radius=[10]
            )

        btn_back.bind(
            on_press=self.go_back,
            pos=lambda instance, pos: setattr(btn_back.rect, 'pos', pos),
            size=lambda instance, size: setattr(btn_back.rect, 'size', size)
        )

        # Добавляем элементы в контейнер
        content_container.add_widget(self.title_label)
        content_container.add_widget(scroll)
        content_container.add_widget(btn_back)

        # Добавляем контейнер в основной layout
        self.main_layout.add_widget(content_container)
        self.add_widget(self.main_layout)

    def update_bg(self, *args):
        self.bg.pos = self.main_layout.pos
        self.bg.size = self.main_layout.size

    def update_content_bg(self, *args):
        self.content_bg.pos = self.main_layout.children[0].pos
        self.content_bg.size = self.main_layout.children[0].size

    def on_pre_enter(self):
        self.update_text()
        self.update_title()

    def update_text(self):
        lang = getattr(self.manager, 'language', 'en')
        text = translations.get(lang, {}).get('AboutUs', 'No information available')
        self.info_label.text = text

    def update_title(self):
        lang = getattr(self.manager, 'language', 'en')
        titles = {
            'en': 'About Us',
            'ru': 'О компании',
            'uz': 'Kompaniya haqida'
        }
        self.title_label.text = titles.get(lang, 'About Us')

    def go_back(self, instance):
        self.manager.current = 'menu'