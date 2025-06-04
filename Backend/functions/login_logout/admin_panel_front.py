from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window

from Backend.ClassesNew.ROLE.bank_worker import BankWorker
from Backend.ClassesNew.ROLE.base_user_m import Role

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.login_input = TextInput(hint_text='Login', multiline=False)
        self.password_input = TextInput(hint_text='Password', password=True, multiline=False)
        login_button = Button(text='Login')
        login_button.bind(on_press=self.login)

        self.message = Label(text='')

        layout.add_widget(self.login_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(self.message)

        self.add_widget(layout)

    def login(self, instance):
        login = self.login_input.text
        password = self.password_input.text

        user = self.authenticate(login, password)
        if user:
            self.manager.current = 'bank_dashboard'
        else:
            self.message.text = "Неверный логин или пароль"

    def authenticate(self, login, password):
        try:
            user = BankWorker.get((BankWorker.login == login) & (BankWorker.password == password))
            roles = user.enter.get().choicefl
            if Role.BANK_WORKER in [r.name for r in roles]:
                return user
            return None
        except BankWorker.DoesNotExist:
            return None

class BankDashboard(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout()
        layout.add_widget(Label(text="Добро пожаловать в админ-панель (банк-работник)"))
        self.add_widget(layout)

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(BankDashboard(name="bank_dashboard"))

        Window.bind(on_key_down=self.on_key_down)
        return self.sm

    def on_key_down(self, window, key, scancode, codepoint, modifier):
        if 'ctrl' in modifier and codepoint == 'b':
            self.sm.current = 'login'

if __name__ == '__main__':
    MyApp().run()
    