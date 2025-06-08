import gettext
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup

# Инициализация переводчика (по умолчанию будет выдавать исходный текст)
gettext.bindtextdomain('app', 'locales')
gettext.textdomain('app')
_ = gettext.gettext


class PhoneEntryScreen(Screen):
    def on_pre_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Подсказка
        layout.add_widget(Label(text=_('Введите номер телефона для пополнения:'), size_hint_y=None, height=30))

        # Поле ввода
        self.phone_input = TextInput(
            hint_text=_('+998901234567'),
            multiline=False,
            size_hint_y=None,
            height=40
        )
        layout.add_widget(self.phone_input)

        # Кнопки
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_confirm = Button(text=_('Подтвердить'))
        btn_back    = Button(text=_('Назад'))

        btn_confirm.bind(on_press=self.on_confirm)
        btn_back.bind(on_press=lambda *a: setattr(self.manager, 'current', 'menu'))

        btn_box.add_widget(btn_confirm)
        btn_box.add_widget(btn_back)
        layout.add_widget(btn_box)

        self.add_widget(layout)

    def on_confirm(self, instance):
        number = self.phone_input.text.strip()
        if not number:
            Popup(
                title=_('Ошибка'),
                content=Label(text=_('Номер не может быть пустым')),
                size_hint=(0.6, 0.3)
            ).open()
            return

        # Сохраняем номер для следующего экрана
        top_up_screen = self.manager.get_screen('top_up_choice')
        top_up_screen.phone_number = number
        self.manager.current = 'top_up_choice'


class TopUpChoiceScreen(Screen):
    def on_pre_enter(self):
        self.build_ui()

    def build_ui(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Показываем номер, который ввёл пользователь
        number = getattr(self, 'phone_number', '')
        layout.add_widget(Label(
                              text=_('Пополнение номера: {num}').format(num=number),
                              size_hint_y=None, height=30
                          ))

        # Кнопки выбора способа
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        btn_card = Button(text=_('Пополнить картой'))
        btn_cash = Button(text=_('Пополнить наличкой'))
        btn_back = Button(text=_('Назад'))

        btn_card.bind(on_press=self.top_up_by_card)
        btn_cash.bind(on_press=self.top_up_by_cash)
        btn_back.bind(on_press=lambda *a: setattr(self.manager, 'current', 'menu'))

        btn_box.add_widget(btn_card)
        btn_box.add_widget(btn_cash)
        btn_box.add_widget(btn_back)
        layout.add_widget(btn_box)

        self.add_widget(layout)

    def top_up_by_card(self, instance):
        number = getattr(self, 'phone_number', '')
        # Ваша логика пополнения картой...
        Popup(
            title=_('Информация'),
            content=Label(text=_('Симуляция: пополнение {num} картой').format(num=number)),
            size_hint=(0.6, 0.3)
        ).open()

    def top_up_by_cash(self, instance):
        number = getattr(self, 'phone_number', '')
        # Ваша логика пополнения наличкой...
        Popup(
            title=_('Информация'),
            content=Label(text=_('Симуляция: пополнение {num} наличкой').format(num=number)),
            size_hint=(0.6, 0.3)
        ).open()
