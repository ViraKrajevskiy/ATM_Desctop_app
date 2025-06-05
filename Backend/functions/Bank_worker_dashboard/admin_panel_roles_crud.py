from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner 

# импорт моделей
from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.ClassesNew.ROLE.bank_worker import BankWorker
from Backend.ClassesNew.ROLE.incasator import Incasator
from Backend.ClassesNew.ROLE.user import User

class DefaultUserTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        scroll = ScrollView()
        grid = GridLayout(cols=7, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'First Name', 'Surname', 'Last Name', 'Created At', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for user in DefaultUser.select():
            grid.add_widget(Label(text=str(user.id)))
            grid.add_widget(Label(text=user.first_name))
            grid.add_widget(Label(text=user.surname))
            grid.add_widget(Label(text=user.last_name))
            grid.add_widget(Label(text=str(user.created_at)))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda x, u=user: self.open_edit_popup(u))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, u=user: self.delete_user(u))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_add_popup(self, instance):
        self.show_user_popup()

    def open_edit_popup(self, user):
        self.show_user_popup(user)

    def show_user_popup(self, user=None):
        is_edit = user is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Input fields for user data
        inp_first = TextInput(text=user.first_name if is_edit else '', hint_text="Имя")
        inp_surname = TextInput(text=user.surname if is_edit else '', hint_text="Фамилия")
        inp_last = TextInput(text=user.last_name if is_edit else '', hint_text="Отчество")

        # Role selection spinner
        role_spinner = Spinner(
            text=user.role.name if is_edit else 'Выберите роль',
            values=[role.name for role in Role.select()],
            size_hint=(1, None),
            height=40
        )

        popup_layout.add_widget(inp_first)
        popup_layout.add_widget(inp_surname)
        popup_layout.add_widget(inp_last)
        popup_layout.add_widget(role_spinner)

        btn_save = Button(text='Сохранить')
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                      content=popup_layout,
                      size_hint=(0.6, 0.5))

        # Update the save binding to include role selection
        btn_save.bind(on_press=lambda x: self.save_user(
                          user,
                          inp_first.text,
                          inp_surname.text,
                          inp_last.text,
                          role_spinner.text,  # Pass selected role name
                          popup
                      ))
        popup.open()


    def save_user(self, user, first_name, surname, last_name, role_name, popup):
        role = Role.get(Role.name == role_name)
        if user:
            user.first_name = first_name
            user.surname = surname
            user.last_name = last_name
            user.role = role
            user.save()
        else:
            user = DefaultUser.create(first_name=first_name, surname=surname, last_name=last_name, role=role)

    # Далее создаём или обновляем связанную таблицу в зависимости от роли
        if role.name == 'User':
            if not hasattr(user, 'user'):
                User.create(connect_id=user.id)
        elif role.name == 'Incasator':
            if not hasattr(user, 'incasator'):
                Incasator.create(login='', password='', default_user_id=user.id)
        elif role.name == 'BankWorker':
            if not hasattr(user, 'bankworker'):
                BankWorker.create(login='', password='')

        popup.dismiss()
        self.build_table()


    def delete_user(self, user):
        user.delete_instance()
        self.build_table()

class RoleTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Создаем контейнер для таблицы
        self.table_container = BoxLayout(orientation='vertical', padding=10)
        self.add_widget(self.table_container)

    def on_pre_enter(self):
        self.build_table()
    def build_table(self):
        container = self.table_container
        container.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_release=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_release=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Name', 'Access', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for role in Role.select():
            grid.add_widget(Label(text=str(role.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=role.name, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(role.access), size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_release=lambda x, r=role: self.open_edit_popup(r))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_release=lambda x, r=role: self.confirm_delete_role(r))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        container.add_widget(layout)

    def open_add_popup(self, instance=None):
        self.show_role_popup()

    def open_edit_popup(self, role):
        self.show_role_popup(role)

    def show_role_popup(self, role=None):
        is_edit = role is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_name = TextInput(text=role.name if is_edit else '', hint_text="Название роли", multiline=False)

    # Для access используем чекбокс
        access_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        access_label = Label(text="Доступ:", size_hint_x=0.7)
        inp_access = CheckBox(active=role.access if is_edit else False)
        access_layout.add_widget(access_label)
        access_layout.add_widget(inp_access)

        popup_layout.add_widget(inp_name)
        popup_layout.add_widget(access_layout)

        btn_save = Button(text='Сохранить', size_hint_y=None, height=40)
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                    content=popup_layout, size_hint=(0.6, 0.5))

        def on_save(instance):
            name = inp_name.text.strip()
            access = inp_access.active  # boolean

            if not name:
                self.show_error_popup('Название роли не может быть пустым.')
                return

            try:
                if role:
                    role.name = name
                    role.access = access
                    role.save()
                else:
                    Role.create(name=name, access=access)
            except Exception as e:
                self.show_error_popup(f'Ошибка при сохранении: {str(e)}')
                return

            popup.dismiss()
            self.build_table()

        btn_save.bind(on_release=on_save)
        popup.open()

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка', size_hint=(0.5, 0.3))
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=message))
        btn_close = Button(text='Закрыть', size_hint_y=None, height=40)
        btn_close.bind(on_release=popup.dismiss)
        box.add_widget(btn_close)
        popup.content = box
        popup.open()

    def confirm_delete_role(self, role):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        content.add_widget(Label(text=f'Удалить роль "{role.name}"?'))

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_yes = Button(text='Да')
        btn_no = Button(text='Нет')

        btn_box.add_widget(btn_yes)
        btn_box.add_widget(btn_no)
        content.add_widget(btn_box)

        popup = Popup(title='Подтверждение удаления', content=content, size_hint=(0.5, 0.3))

        def delete_and_close(instance):
            try:
                role.delete_instance()
                self.build_table()
            except Exception as e:
                self.show_error_popup(f'Ошибка при удалении: {str(e)}')
            popup.dismiss()

        btn_yes.bind(on_release=delete_and_close)
        btn_no.bind(on_release=popup.dismiss)

        popup.open()

class BankWorkerTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Кнопки назад и добавить
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        # Таблица с прокруткой
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Login', 'Password', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for worker in BankWorker.select():
            grid.add_widget(Label(text=str(worker.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=worker.login, size_hint_y=None, height=30))
            grid.add_widget(Label(text=worker.password, size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda x, w=worker: self.open_edit_popup(w))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, w=worker: self.delete_worker(w))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка', size_hint=(0.5, 0.3))
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=message))
        btn_close = Button(text='Закрыть', size_hint_y=None, height=40)
        btn_close.bind(on_release=popup.dismiss)
        box.add_widget(btn_close)
        popup.content = box
        popup.open()


    def open_add_popup(self, instance):
        self.show_worker_popup()

    def open_edit_popup(self, worker):
        self.show_worker_popup(worker)

    def show_worker_popup(self, worker=None):
        is_edit = worker is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_login = TextInput(text=worker.login if is_edit else '', hint_text="Логин")
        inp_password = TextInput(text=worker.password if is_edit else '', hint_text="Пароль", password=True)

        popup_layout.add_widget(inp_login)
        popup_layout.add_widget(inp_password)

        btn_save = Button(text='Сохранить')
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                      content=popup_layout, size_hint=(0.6, 0.4))
        btn_save.bind(on_press=lambda x: self.save_worker(worker, inp_login.text, inp_password.text, popup))
        popup.open()

    def save_worker(self, worker, login, password, popup):
        if not login or not password:
            self.show_error_popup('Логин и пароль не могут быть пустыми.')
            return

        if worker:
            worker.login = login
            worker.password = password
            worker.save()
        else:
            BankWorker.create(login=login, password=password)
        popup.dismiss()
        self.build_table()


    def delete_worker(self, worker):
        worker.delete_instance()
        self.build_table()

class IncasatorTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        scroll = ScrollView()
        grid = GridLayout(cols=7, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'First Name', 'Surname', 'Last Name', 'Created At', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for user in DefaultUser.select():
            grid.add_widget(Label(text=str(user.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=user.first_name, size_hint_y=None, height=30))
            grid.add_widget(Label(text=user.surname, size_hint_y=None, height=30))
            grid.add_widget(Label(text=user.last_name, size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(user.created_at), size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda x, u=user: self.open_edit_popup(u))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, u=user: self.delete_user(u))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_add_popup(self, instance):
        self.show_user_popup()

    def open_edit_popup(self, user):
        self.show_user_popup(user)

    def show_user_popup(self, user=None):
        is_edit = user is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_first = TextInput(text=user.first_name if is_edit else '', hint_text="Имя")
        inp_surname = TextInput(text=user.surname if is_edit else '', hint_text="Фамилия")
        inp_last = TextInput(text=user.last_name if is_edit else '', hint_text="Отчество")

        popup_layout.add_widget(inp_first)
        popup_layout.add_widget(inp_surname)
        popup_layout.add_widget(inp_last)

        btn_save = Button(text='Сохранить')
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                      content=popup_layout, size_hint=(0.6, 0.5))
        btn_save.bind(on_press=lambda x: self.save_user(user, inp_first.text, inp_surname.text, inp_last.text, popup))
        popup.open()

    def save_user(self, user, first_name, surname, last_name, popup):
        if user:
            user.first_name = first_name
            user.surname = surname
            user.last_name = last_name
            user.save()
        else:
            DefaultUser.create(first_name=first_name, surname=surname, last_name=last_name)
        popup.dismiss()
        self.build_table()

    def delete_user(self, user):
        user.delete_instance()
        self.build_table()


class UserTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Connect DefaultUser ID', 'Wallet Count', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for user in User.select():
            grid.add_widget(Label(text=str(user.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(user.connect.id) if user.connect else "None", size_hint_y=None, height=30))
            wallets_count = user.wallet.count() if hasattr(user, 'wallet') else 0
            grid.add_widget(Label(text=str(wallets_count), size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda x, u=user: self.open_edit_popup(u))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, u=user: self.delete_user(u))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_add_popup(self, instance):
        self.show_user_popup()

    def open_edit_popup(self, user):
        self.show_user_popup(user)

    def show_user_popup(self, user=None):
        is_edit = user is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Для связанного DefaultUser — можно сделать поле ввода ID (число)
        inp_connect_id = TextInput(text=str(user.connect.id) if is_edit and user.connect else '', hint_text="Connect DefaultUser ID", input_filter='int')

        popup_layout.add_widget(inp_connect_id)

        btn_save = Button(text='Сохранить')
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                      content=popup_layout, size_hint=(0.6, 0.4))
        btn_save.bind(on_press=lambda x: self.save_user(user, inp_connect_id.text, popup))
        popup.open()

    def save_user(self, user, connect_id_text, popup):
        try:
            connect_id = int(connect_id_text)
            connect_obj = DefaultUser.get(DefaultUser.id == connect_id)
        except Exception:
            # Не валидный connect_id
            return

        if user:
            user.connect = connect_obj
            user.save()
        else:
            User.create(connect=connect_obj)
        popup.dismiss()
        self.build_table()

    def delete_user(self, user):
        user.delete_instance()
        self.build_table()