from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput


# импорт моделей
from Backend.ClassesNew.ROLE.base_user_m import DefaultUser, Role
from Backend.ClassesNew.ROLE.bank_worker import BankWorker
from Backend.ClassesNew.ROLE.incasator import Incasator
from Backend.ClassesNew.ROLE.user import User
from Backend.ClassesNew.CASH.wallet import Wallet, WalletMoney

from Backend.data_base.core import db

class DefaultUserTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def show_error_popup(self, message):
        popup = Popup(
            title='Ошибка',
            content=Label(text=message),
            size_hint=(0.5, 0.3)
        )
        popup.open()

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
    # Проверка пустых полей и роли
        if not first_name.strip() or not surname.strip() or not last_name.strip() or role_name == 'Выберите роль':
            self.show_error_popup('Пожалуйста, заполните все поля и выберите роль.')
            return
        try:
            with db.atomic():  # Transaction for consistency
                role = Role.get(Role.name == role_name)

                if user:
                # Update existing user
                    user.first_name = first_name
                    user.surname = surname
                    user.last_name = last_name
                    user.role = role
                    user.save()
                else:
                # Create new user
                    user = DefaultUser.create(
                        first_name=first_name,
                        surname=surname,
                        last_name=last_name,
                        role=role
                )

            # Handle role-specific records
                if role.name == Role.USER:
                    User.get_or_create(connect=user)
                elif role.name == Role.INCOSATOR:
                    Incasator.get_or_create(
                        default_user=user,
                        defaults={'login': '', 'password': ''})
                elif role.name == Role.BANK_WORKER:
                    BankWorker.get_or_create(
                        user=user,
                        defaults={'login': '', 'password': ''})

            popup.dismiss()
            self.build_table()

        except Exception as e:
            self.show_error_popup(f'Ошибка сохранения: {str(e)}')


    def delete_user(self, user):
        try:
            with db.atomic():
            # Delete role-specific record first
                if user.role.name == Role.USER and hasattr(user, 'user'):
                    user.user.delete_instance()
                elif user.role.name == Role.INCOSATOR and hasattr(user, 'incasator'):
                    user.incasator.delete_instance()
                elif user.role.name == Role.BANK_WORKER and hasattr(user, 'bank_worker'):
                    user.bank_worker.delete_instance()

                user.delete_instance()
            self.build_table()
        except Exception as e:
            self.show_error_popup(f'Ошибка удаления: {str(e)}')

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

        try:
            with db.atomic():  # Use transaction for data consistency
                if worker:
                # Update existing worker
                    worker.login = login
                    worker.password = password
                    worker.save()
                else:
                # Create new worker with default user
                    default_user = DefaultUser.create(
                    first_name="Bank",
                    surname="Worker",
                    last_name=login,  # Using login as last name
                    role=Role.get(name=Role.BANK_WORKER)
                )

                    BankWorker.create(
                    login=login,
                    password=password,
                    user=default_user
                )
            popup.dismiss()
            self.build_table()

        except Exception as e:
            self.show_error_popup(f'Ошибка сохранения: {str(e)}')


    def delete_worker(self, worker):
        try:
            with db.atomic():
                user = worker.user
                worker.delete_instance()
                user.delete_instance()  # Delete the associated user
            self.build_table()
        except Exception as e:
            self.show_error_popup(f'Ошибка удаления: {str(e)}')


class IncasatorTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_text = ''

    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        root_layout = BoxLayout(orientation='vertical', padding=10)

        # Фильтр
        filter_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        filter_input = TextInput(
            text=self.filter_text,
            hint_text="Фильтр по логину",
            multiline=False
        )
        btn_apply = Button(text='Применить', size_hint_x=None, width=100)
        btn_apply.bind(on_press=lambda inst: self.on_apply_filter(filter_input.text))
        filter_box.add_widget(filter_input)
        filter_box.add_widget(btn_apply)
        root_layout.add_widget(filter_box)

        # Кнопки управления
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)
        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        root_layout.add_widget(btn_box)

        # Таблица
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        # Заголовки
        headers = ['ID', 'Логин', 'Пароль', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        # Данные
        query = Incasator.select()
        if self.filter_text.strip():
            query = query.where(Incasator.login.contains(self.filter_text))

        for incasator in query:
            grid.add_widget(Label(text=str(incasator.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=incasator.login, size_hint_y=None, height=30))
            grid.add_widget(Label(text=incasator.password, size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda x, i=incasator: self.open_edit_popup(i))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, i=incasator: self.delete_incasator(i))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        root_layout.add_widget(scroll)
        self.add_widget(root_layout)

    def on_apply_filter(self, new_text):
        self.filter_text = new_text
        self.build_table()

    def open_add_popup(self, instance=None):
        self.show_incasator_popup()

    def open_edit_popup(self, incasator):
        self.show_incasator_popup(incasator)

    def show_incasator_popup(self, incasator=None):
        is_edit = incasator is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Поля для логина и пароля
        inp_login = TextInput(text=incasator.login if is_edit else '', hint_text="Логин")
        inp_password = TextInput(
            text=incasator.password if is_edit else '',
            hint_text="Пароль",
            password=True
        )

        popup_layout.add_widget(inp_login)
        popup_layout.add_widget(inp_password)

        btn_save = Button(text='Сохранить')
        popup_layout.add_widget(btn_save)

        popup_title = 'Редактирование инкассатора' if is_edit else 'Добавление инкассатора'
        popup = Popup(title=popup_title, content=popup_layout, size_hint=(0.6, 0.4))

        btn_save.bind(on_press=lambda x: self.save_incasator(
                          incasator,
                          inp_login.text,
                          inp_password.text,
                          popup
                      ))
        popup.open()

    def save_incasator(self, incasator, login, password, popup):
        if not login or not password:
            self.show_error_popup('Логин и пароль не могут быть пустыми')
            return

        try:
            with db.atomic():
                if incasator:
                    # Обновляем существующего инкассатора
                    incasator.login = login
                    incasator.password = password
                    incasator.save()
                else:
                    # Создаем нового инкассатора с дефолтным пользователем
                    default_user = DefaultUser.create(
                        first_name="Инкассатор",
                        surname=login,  # Используем логин как фамилию
                        last_name="",
                        role=Role.get(name=Role.INCOSATOR)
                    )
                    Incasator.create(
                        login=login,
                        password=password,
                        default_user=default_user
                    )

            popup.dismiss()
            self.build_table()
        except Exception as e:
            self.show_error_popup(f'Ошибка сохранения: {str(e)}')

    def delete_incasator(self, incasator):
        try:
            with db.atomic():
                user = incasator.default_user
                incasator.delete_instance()
                user.delete_instance()
            self.build_table()
        except Exception as e:
            self.show_error_popup(f'Ошибка удаления: {str(e)}')

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка', size_hint=(0.5, 0.3))
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(Label(text=message))
        btn_close = Button(text='Закрыть', size_hint_y=None, height=40)
        btn_close.bind(on_release=popup.dismiss)
        box.add_widget(btn_close)
        popup.content = box
        popup.open()


class UserTable(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filter_text = ''

    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Фильтр
        filter_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        filter_input = TextInput(text=self.filter_text,
                                 hint_text="Фильтр по Connect DefaultUser ID",
                                 multiline=False)
        btn_apply = Button(text="Применить", size_hint_x=None, width=100)
        btn_apply.bind(on_press=lambda inst: self.on_apply_filter(filter_input.text))
        filter_box.add_widget(filter_input)
        filter_box.add_widget(btn_apply)
        layout.add_widget(filter_box)

        # Навигация
        nav_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda _: setattr(self.manager, 'current', 'bank_dashboard'))
        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)
        nav_box.add_widget(btn_back)
        nav_box.add_widget(btn_add)
        layout.add_widget(nav_box)

        # Таблица
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Connect DefaultUser ID', 'WalletMoney ID', 'Редакт.', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True,
                                  size_hint_y=None, height=30))

        query = User.select()
        if self.filter_text.strip():
            try:
                fid = int(self.filter_text.strip())
                query = query.where(User.connect_id == fid)
            except ValueError:
                pass

        for usr in query:
            grid.add_widget(Label(text=str(usr.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(usr.connect.id) if usr.connect else "None",
                                  size_hint_y=None, height=30))
            wm_ids = [str(wm.id) for wm in usr.wallet]  # ManyToMany
            grid.add_widget(Label(text=",".join(wm_ids) if wm_ids else "None",
                                  size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=lambda inst, u=usr: self.open_edit_popup(u))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda inst, u=usr: self.delete_user(u))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def on_apply_filter(self, text):
        self.filter_text = text
        self.build_table()

    def open_add_popup(self, instance=None):
        self.show_user_popup()

    def open_edit_popup(self, user_obj):
        self.show_user_popup(user_obj)

    def show_user_popup(self, user_obj=None):
        is_edit = user_obj is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_connect = TextInput(text=str(user_obj.connect.id) if is_edit and user_obj.connect else '',
                                hint_text="Connect DefaultUser ID",
                                input_filter='int', multiline=False)
        popup_layout.add_widget(inp_connect)

        # Spinner WalletMoney
        wm_list = list(WalletMoney.select())
        wm_vals = [f"{wm.id}: W{wm.wallet.id} ({wm.money.money_nominal}×{wm.quantity})" for wm in wm_list]
        spinner_wm = Spinner(
            text=wm_vals[0] if is_edit and user_obj.wallet else 'Выберите WalletMoney',
            values=wm_vals,
            size_hint_y=None, height=40
        )
        popup_layout.add_widget(Label(text='Привязать к WalletMoney:'))
        popup_layout.add_widget(spinner_wm)

        btn_save = Button(text='Сохранить', size_hint_y=None, height=40)
        popup_layout.add_widget(btn_save)

        popup = Popup(title='Редактирование' if is_edit else 'Добавление',
                      content=popup_layout,
                      size_hint=(0.7, 0.6))
        popup.open()

        def do_save(inst):
            # Работаем с переменной user
            if is_edit:
                usr = user_obj
            else:
                # создаём нового
                try:
                    cid = int(inp_connect.text)
                    connect_obj = DefaultUser.get_by_id(cid)
                except Exception:
                    print(f"Ошибка connect_id: {inp_connect.text}")
                    return
                usr = User.create(connect=connect_obj)

            # Если редактирование, обновляем connect
            if is_edit:
                try:
                    cid = int(inp_connect.text)
                    connect_obj = DefaultUser.get_by_id(cid)
                    usr.connect = connect_obj
                    usr.save()
                except Exception:
                    print(f"Ошибка connect_id: {inp_connect.text}")

            # Привязка WalletMoney
            try:
                wm_id = int(spinner_wm.text.split(':', 1)[0])
                wm_obj = WalletMoney.get_by_id(wm_id)
                usr.wallet.clear()
                usr.wallet.add(wm_obj)
            except Exception:
                print(f"Ошибка WalletMoney: {spinner_wm.text}")

            popup.dismiss()
            self.build_table()

        btn_save.bind(on_press=do_save)

    def delete_user(self, user_obj):
        user_obj.delete_instance(recursive=True)
        self.build_table()
