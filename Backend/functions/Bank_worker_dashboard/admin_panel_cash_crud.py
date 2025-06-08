from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup

from peewee import fn

from Backend.ClassesNew.CASH import wallet
from Backend.data_base.core import db
from Backend.ClassesNew.CASH.credit_cards import CreditCards,PhoneNumber
from Backend.ClassesNew.CASH.money import Money
from Backend.ClassesNew.CASH.wallet import Wallet

from Backend.ClassesNew.CASH.money import Money

class PhoneNumberTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Верхняя панель с кнопками
        btn_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        btn_box.add_widget(btn_back)
        btn_box.add_widget(btn_add)
        layout.add_widget(btn_box)

        # Таблица с данными
        scroll = ScrollView()
        grid = GridLayout(cols=4, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Phone Number', 'Balance', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for phone in PhoneNumber.select():
            grid.add_widget(Label(text=str(phone.id)))
            grid.add_widget(Label(text=phone.phone_number))
            grid.add_widget(Label(text=str(phone.balance)))

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=lambda x, p=phone: self.delete_phone(p))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_add_popup(self, instance):
        self.show_phone_popup()

    def show_phone_popup(self, phone=None):
        is_edit = phone is not None
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        hbox = BoxLayout(size_hint_y=None, height=40)

        prefix_label = Label(text='+998', size_hint_x=0.3)
        inp_number = TextInput(
            text=phone.phone_number[4:] if is_edit and phone.phone_number.startswith('+998') else '',
            hint_text='Номер (без +998)',
            input_filter='int',
            multiline=False)

        hbox.add_widget(prefix_label)
        hbox.add_widget(inp_number)

        inp_balance = TextInput(
            text=str(phone.balance) if is_edit else '',
            hint_text='Баланс',
            input_filter='int',
            multiline=False)

        popup_layout.add_widget(hbox)
        popup_layout.add_widget(inp_balance)

        btn_save = Button(text='Сохранить', size_hint_y=None, height=40)
        popup_layout.add_widget(btn_save)

        popup = Popup(
            title='Редактирование' if is_edit else 'Добавление',
            content=popup_layout,
            size_hint=(0.5, 0.4),
            auto_dismiss=False)

        btn_save.bind(on_press=lambda x: self.save_phone(phone, inp_number.text, inp_balance.text, popup))
        popup.open()

    def save_phone(self, phone, number_without_prefix, balance, popup):
        try:
            number_clean = number_without_prefix.strip()
            if not number_clean.isdigit():
                raise ValueError("Номер должен содержать только цифры")

            if len(number_clean) != 9:
                raise ValueError("Введите ровно 9 цифр (без +998)")

            full_number = '+998' + number_clean

            if len(full_number) != 13:
                raise ValueError("Итоговый номер должен быть длиной 13 символов")

            with db.atomic():
                if phone:
                    phone.phone_number = full_number
                    phone.balance = int(balance)
                    phone.save()
                else:
                    PhoneNumber.create(phone_number=full_number, balance=int(balance))

            popup.dismiss()
            self.build_table()

        except Exception as e:
            self.show_error_popup(f'Ошибка: {e}')


    def delete_phone(self, phone):
        try:
            with db.atomic():
                phone.delete_instance()
            self.build_table()
        except Exception as e:
            self.show_error_popup(f'Ошибка удаления: {e}')

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка',
                      content=Label(text=message),
                      size_hint=(0.5, 0.3))
        popup.open()


from functools import partial
from datetime import datetime

class CreditCardTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        top = BoxLayout(size_hint_y=None, height=40)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=self.open_add_popup)

        top.add_widget(btn_back)
        top.add_widget(btn_add)
        layout.add_widget(top)

        scroll = ScrollView()
        grid = GridLayout(cols=7, size_hint_y=None)  # теперь 7 колонок (ID, Number, Balance, Phones, Редактировать, Удалить)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Card Number', 'Balance', 'Phone Numbers', 'Редактировать', 'Удалить']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for card in CreditCards.select():
            grid.add_widget(Label(text=str(card.id)))
            grid.add_widget(Label(text=str(card.card_number)))
            grid.add_widget(Label(text=str(card.balance)))
            phones = ", ".join(p.phone_number for p in card.phone_field)
            grid.add_widget(Label(text=phones))

            btn_edit = Button(text="✏️", size_hint_y=None, height=30)
            btn_edit.bind(on_press=partial(self.open_edit_popup, card.id))
            grid.add_widget(btn_edit)

            btn_del = Button(text="🗑️", size_hint_y=None, height=30)
            btn_del.bind(on_press=partial(self.delete_card, card.id))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_add_popup(self, instance):
        self.show_card_popup()

    def open_edit_popup(self, card_id, instance):
        card = CreditCards.get_by_id(card_id)
        self.show_card_popup(card)

    def show_card_popup(self, card=None):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_card_number = TextInput(hint_text='Номер карты', input_filter='int')
        inp_balance = TextInput(hint_text='Баланс', input_filter='int')
        inp_password = TextInput(hint_text='Пароль', input_filter='int')  # security_code
        inp_cvv = TextInput(hint_text='CVV')  # special_identificator
        inp_bank_name = TextInput(hint_text='Название банка')
        inp_card_type = TextInput(hint_text='Тип карты')
        inp_end_date = TextInput(hint_text='Дата окончания (YYYY-MM-DD)')

        # Если редактируем - заполнить поля значениями
        if card:
            inp_card_number.text = str(card.card_number)
            inp_balance.text = str(card.balance)
            inp_password.text = str(card.security_code)
            inp_cvv.text = card.special_identificator
            inp_bank_name.text = card.bank_name
            inp_card_type.text = card.card_type
            inp_end_date.text = card.card_end_date.strftime('%Y-%m-%d') if card.card_end_date else ''

        layout.add_widget(inp_card_number)
        layout.add_widget(inp_balance)
        layout.add_widget(inp_password)
        layout.add_widget(inp_cvv)
        layout.add_widget(inp_bank_name)
        layout.add_widget(inp_card_type)
        layout.add_widget(inp_end_date)

        phone_checks = []
        for phone in PhoneNumber.select():
            hbox = BoxLayout(size_hint_y=None, height=30)
            checkbox = CheckBox()
            label = Label(text=phone.phone_number)
            hbox.add_widget(checkbox)
            hbox.add_widget(label)
            layout.add_widget(hbox)
            phone_checks.append((checkbox, phone))

            # Отметить уже привязанные номера при редактировании
            if card and phone in card.phone_field:
                checkbox.active = True

        btn_save = Button(text='Сохранить')
        layout.add_widget(btn_save)

        title = 'Редактировать карту' if card else 'Добавить карту'
        popup = Popup(title=title, content=layout, size_hint=(0.7, 0.9))
        popup.open()

        def save_card(instance):
            try:
                with db.atomic():
                    if card:
                        # Обновление существующей карты
                        card.card_number = int(inp_card_number.text)
                        card.balance = int(inp_balance.text)
                        card.security_code = int(inp_password.text)
                        card.special_identificator = inp_cvv.text
                        card.bank_name = inp_bank_name.text
                        card.card_type = inp_card_type.text
                        card.card_end_date = datetime.strptime(inp_end_date.text, '%Y-%m-%d').date()
                        card.save()

                        # Обновление связей с номерами
                        card.phone_field.clear()
                        for checkbox, phone in phone_checks:
                            if checkbox.active:
                                card.phone_field.add(phone)

                    else:
                        # Создание новой карты
                        new_card = CreditCards.create(
                            card_number=int(inp_card_number.text),
                            balance=int(inp_balance.text),
                            security_code=int(inp_password.text),
                            special_identificator=inp_cvv.text,
                            bank_name=inp_bank_name.text,
                            card_type=inp_card_type.text,
                            card_end_date=datetime.strptime(inp_end_date.text, '%Y-%m-%d').date())
                        for checkbox, phone in phone_checks:
                            if checkbox.active:
                                new_card.phone_field.add(phone)

                popup.dismiss()
                self.build_table()
            except Exception as e:
                self.show_error_popup(f"Ошибка при сохранении: {e}")

        btn_save.bind(on_press=save_card)

    def delete_card(self, card_id, *args):
        try:
            with db.atomic():
                card = CreditCards.get_by_id(card_id)
            # удаляем только саму карту и её связь с телефонами
            # (через delete_instance(recursive=False), тогда ManyToMany не трогается)
                card.delete_instance(recursive=False)
            self.build_table()
        except Exception as e:
            self.show_error_popup(f"Ошибка удаления: {e}")


    def show_error_popup(self, msg):
        popup = Popup(title='Ошибка', content=Label(text=msg), size_hint=(0.5, 0.3))
        popup.open()
        
class MoneyManagementScreen(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Top buttons
        top = BoxLayout(size_hint_y=None, height=40)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))

        btn_add_money = Button(text='Добавить деньги')
        btn_add_money.bind(on_press=lambda x: self.show_money_popup())

        top.add_widget(btn_back)
        top.add_widget(btn_add_money)
        layout.add_widget(top)

        self.show_money_table(layout)
        self.add_widget(layout)

    def delete_money(self, money):
        # Пример удаления объекта money из БД
        try:
            money.delete_instance()
            print(f"[INFO] Удалены данные: {money}")
            self.build_table()  # обновить интерфейс
        except Exception as e:
            print(f"[ERROR] Не удалось удалить: {e}")

    def show_money_table(self, main_layout):
        if hasattr(self, 'table_container'):
            main_layout.remove_widget(self.table_container)

        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Номинал', 'Тип', 'Дата создания', 'Действия']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for money in Money.select():
            grid.add_widget(Label(text=str(money.money_id)))
            grid.add_widget(Label(text=str(money.money_nominal)))
            grid.add_widget(Label(text=money.types))
            grid.add_widget(Label(text=str(money.date_made)))

            actions = BoxLayout(size_hint_y=None, height=30)
            btn_edit = Button(text="✏️")
            btn_edit.bind(on_press=lambda x, m=money: self.show_money_popup(m))
            btn_del = Button(text="🗑️")
            btn_del.bind(on_press=lambda x, m=money: self.delete_money(m))

            actions.add_widget(btn_edit)
            actions.add_widget(btn_del)
            grid.add_widget(actions)

        scroll.add_widget(grid)
        self.table_container = scroll
        main_layout.add_widget(scroll)

    def show_money_popup(self, money_instance=None):
        is_edit = money_instance is not None
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_nominal = TextInput(
            hint_text='Номинал',
            input_filter='int',
            text=str(money_instance.money_nominal) if is_edit else '')
        inp_type = TextInput(
            hint_text='Тип',
            text=money_instance.types if is_edit else '')
        inp_date = TextInput(
            hint_text='Дата создания (YYYY-MM-DD HH:MM:SS)',
            text=str(money_instance.date_made) if is_edit else str(datetime.now()))

        layout.add_widget(inp_nominal)
        layout.add_widget(inp_type)
        layout.add_widget(inp_date)

        btn_save = Button(text='Сохранить')
        layout.add_widget(btn_save)

        popup = Popup(
            title='Редактировать деньги' if is_edit else 'Добавить деньги',
            content=layout,
            size_hint=(0.7, 0.5)
        )
        popup.open()

        def save_money(instance):
            try:
                with db.atomic():
                    if is_edit:
                        money_instance.money_nominal = int(inp_nominal.text)
                        money_instance.types = inp_type.text
                        money_instance.date_made = inp_date.text
                        money_instance.save()
                    else:
                        Money.create(
                            money_nominal=int(inp_nominal.text),
                            types=inp_type.text,
                            date_made=inp_date.text)
                popup.dismiss()
                self.build_table()
            except Exception as e:
                self.show_error_popup(f"Ошибка при сохранении: {e}")

        btn_save.bind(on_press=save_money)


    def show_error_popup(self, msg):
        popup = Popup(title='Ошибка', content=Label(text=msg), size_hint=(0.5, 0.3))
        popup.open()



class WalletTable(Screen):

    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        main = BoxLayout(orientation='vertical', padding=10)
        self.add_widget(main)

        # Верхняя панель
        header = BoxLayout(size_hint_y=None, height=40, spacing=5)
        header.add_widget(Button(text='Назад',
                                 on_press=lambda *_: setattr(self.manager, 'current', 'bank_dashboard')))
        header.add_widget(Button(text='Добавить',
                                 on_press=lambda *_: self.show_popup()))
        main.add_widget(header)

        # Таблица
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        # Заголовки
        for title in ['ID', 'Карта', 'Номинал', 'Редакт.', 'Удалить']:
            grid.add_widget(Label(text=f'[b]{title}[/b]', markup=True,
                                  size_hint_y=None, height=30))

        # Строки таблицы
        for w in Wallet.select():
            grid.add_widget(Label(text=str(w.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(w.card.card_number), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(w.money.money_nominal), size_hint_y=None, height=30))

            # Кнопка редактирования
            grid.add_widget(Button(text='✏️', size_hint_y=None, height=30,
                                   on_press=partial(self.show_popup, w.id)))
            # Кнопка удаления
            grid.add_widget(Button(text='🗑️', size_hint_y=None, height=30,
                                   on_press=partial(self.delete_wallet, w.id)))

        scroll.add_widget(grid)
        main.add_widget(scroll)

    def show_popup(self, wallet_id=None, *_):
        """Показать окно создания/редактирования записи Wallet."""
        is_edit = wallet_id is not None
        popup = Popup(title='Редактировать' if is_edit else 'Добавить',
                      size_hint=(0.8, 0.8))

        box = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Выбор карты
        box.add_widget(Label(text='Выберите карту:', size_hint_y=None, height=30))
        cards = [(CheckBox(group='card'), c) for c in CreditCards.select()]
        if not cards:
            box.add_widget(Label(text='Нет доступных карт'))
        for cb, c in cards:
            row = BoxLayout(size_hint_y=None, height=30)
            row.add_widget(cb)
            row.add_widget(Label(text=str(c.card_number)))
            box.add_widget(row)

        # Выбор номинала
        box.add_widget(Label(text='Выберите номинал:', size_hint_y=None, height=30))
        money_options = [(CheckBox(group='money'), m) for m in Money.select()]
        if not money_options:
            box.add_widget(Label(text='Нет доступных номиналов'))
        for cb, m in money_options:
            row = BoxLayout(size_hint_y=None, height=30)
            row.add_widget(cb)
            row.add_widget(Label(text=str(m.money_nominal)))
            box.add_widget(row)

        # При редактировании отмечаем текущие значения
        if is_edit:
            existing = Wallet.get_by_id(wallet_id)
            for cb, c in cards:
                if c.card_id == existing.card.card_id:
                    cb.active = True
            for cb, m in money_options:
                if m.money_id == existing.money.money_id:
                    cb.active = True

        # Кнопка сохранить
        save_btn = Button(text='Сохранить', size_hint_y=None, height=40)
        box.add_widget(save_btn)
        popup.content = box
        popup.open()

        def save(*_):
            try:
                # Находим выбранные объекты
                card = next(c for cb, c in cards if cb.active)
                money = next(m for cb, m in money_options if cb.active)

                with db.atomic():
                    if is_edit:
                        w = Wallet.get_by_id(wallet_id)
                        w.card = card
                        w.money = money
                        w.save()
                    else:
                        # Проверка на дубликат
                        exists = Wallet.select().where(
                            (Wallet.card == card) &
                            (Wallet.money == money)
                        ).exists()
                        if exists:
                            self.show_error("Такая запись уже существует")
                            return
                        Wallet.create(card=card, money=money)

                popup.dismiss()
                self.build_table()

            except StopIteration:
                self.show_error("Нужно выбрать и карту, и номинал")
            except Exception as e:
                popup.dismiss()
                self.show_error(f"Ошибка: {e}")

        save_btn.bind(on_press=save)

    def delete_wallet(self, wid, *_):
        """Удалить запись и обновить таблицу."""
        try:
            with db.atomic():
                Wallet.get_by_id(wid).delete_instance()
            self.build_table()
        except Exception as e:
            self.show_error(f"Ошибка удаления: {e}")

    def show_error(self, msg):
        Popup(title='Ошибка', content=Label(text=msg),
              size_hint=(0.5, 0.3)).open()
