from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty
from Backend.ClassesNew.ROLE.bank_worker import BankWorker

class LoginScreen(Screen):
    text_key = StringProperty()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(0.6078, 0.7882, 0.8117, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.message_label = Label(text='Введите логин и пароль', markup=True)
        self.login_input = TextInput(hint_text='Логин', multiline=False)
        self.password_input = TextInput(hint_text='Пароль', multiline=False, password=True)
        login_button = Button(text='Войти')
        login_button.bind(on_press=self.verify_credentials)

        layout.add_widget(self.message_label)
        layout.add_widget(self.login_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def verify_credentials(self, instance):
        login = self.login_input.text.strip()
        password = self.password_input.text.strip()

        try:
            worker = BankWorker.get(BankWorker.login == login, BankWorker.password == password)
            self.manager.current = 'bank_dashboard'
        except BankWorker.DoesNotExist:
            self.message_label.text = '[color=ff0000]Неверный логин или пароль[/color]'
            # Убедись, что markup включен
            self.message_label.markup = True