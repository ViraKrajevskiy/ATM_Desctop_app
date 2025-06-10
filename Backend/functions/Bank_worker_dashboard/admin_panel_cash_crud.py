
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup


from functools import partial
from datetime import datetime


from Backend.data_base.core import db
from Backend.ClassesNew.CASH.credit_cards import CreditCards,PhoneNumber
from Backend.ClassesNew.CASH.wallet import Wallet, WalletMoney

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


class CreditCardTable(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Верхняя панель
        top = BoxLayout(size_hint_y=None, height=40)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        btn_add = Button(text='Добавить')
        btn_add.bind(on_press=lambda x: self.show_card_popup())
        top.add_widget(btn_back)
        top.add_widget(btn_add)
        layout.add_widget(top)

        # Таблица
        scroll = ScrollView()
        grid = GridLayout(cols=6, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Card Number', 'Balance', 'Phones', '✏️', '🗑️']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for card in CreditCards.select():
            grid.add_widget(Label(text=str(card.card_id),            size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(card.card_number),        size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(card.balance),            size_hint_y=None, height=30))
            phones = ", ".join(p.phone_number for p in card.phone_field)
            grid.add_widget(Label(text=phones or "—",                size_hint_y=None, height=30))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=partial(self.open_edit_popup, card.card_id))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=partial(self.delete_card, card.card_id))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)
        self.add_widget(layout)

    def open_edit_popup(self, card_id, *args):
        try:
            card = CreditCards.get_by_id(card_id)
        except CreditCards.DoesNotExist:
            self.show_error_popup(f"Карта #{card_id} не найдена.")
            return
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
            if card and phone in list(card.phone_field):
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

        # Верхняя панель с кнопками
        header = BoxLayout(size_hint_y=None, height=40, spacing=5)
        header.add_widget(Button(text='Back',
                                 on_press=lambda *_: setattr(self.manager, 'current', 'bank_dashboard')))
        header.add_widget(Button(text='Add Wallet',
                                 on_press=lambda *_: self.show_add_wallet_popup()))
        main.add_widget(header)

        # Таблица кошельков
        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['Wallet ID', 'Card Number', 'Actions']
        for title in headers:
            grid.add_widget(Label(text=f'[b]{title}[/b]', markup=True, size_hint_y=None, height=30))

        for wallet in Wallet.select():
            grid.add_widget(Label(text=str(wallet.id)))
            grid.add_widget(Label(text=str(wallet.card.card_number)))

            actions = BoxLayout(spacing=5, size_hint_y=None, height=30)
            btn_view = Button(text='View Bills', size_hint_x=0.5)
            btn_view.bind(on_press=partial(self.show_wallet_money_popup, wallet))
            actions.add_widget(btn_view)

            btn_del = Button(text='🗑️', size_hint_x=0.5)
            btn_del.bind(on_press=partial(self.delete_wallet, wallet.id))
            actions.add_widget(btn_del)

            grid.add_widget(actions)

        scroll.add_widget(grid)
        main.add_widget(scroll)
        self.add_widget(main)

    def show_add_wallet_popup(self):
        popup = Popup(title='Add Wallet', size_hint=(0.6, 0.6))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        card_scroll = ScrollView(size_hint=(1, None), height=300)
        card_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        card_list.bind(minimum_height=card_list.setter('height'))

        self.card_btns = []
        for card in CreditCards.select():
            btn = Button(text=f"Card #{card.card_number}", size_hint_y=None, height=40)
            btn.card = card
            self.card_btns.append(btn)
            card_list.add_widget(btn)
        card_scroll.add_widget(card_list)
        layout.add_widget(Label(text="Select Card for Wallet:"))
        layout.add_widget(card_scroll)

        btn_save = Button(text="Create Wallet", size_hint_y=None, height=40)
        layout.add_widget(btn_save)

        self.selected_card = None

        for btn in self.card_btns:
            btn.bind(on_press=self.select_card)

        popup.content = layout
        popup.open()

        def save_wallet(instance):
            try:
                if not self.selected_card:
                    raise ValueError("Card not selected")
                Wallet.create(card=self.selected_card)
                popup.dismiss()
                self.build_table()
            except Exception as e:
                self.show_error(str(e))

        btn_save.bind(on_press=save_wallet)

    def select_card(self, instance):
        self.selected_card = instance.card
        for btn in self.card_btns:
            btn.background_color = (1, 1, 1, 1)
        instance.background_color = (0, 1, 0, 1)

    def select_money(self, instance):
        # Запоминаем выбранный номинал
        self.selected_money = instance.money
        # Сбрасываем подсветку у всех кнопок номиналов
        for btn in self.money_btns:
            btn.background_color = (1, 1, 1, 1)
        # Подсвечиваем выбранную кнопку
        instance.background_color = (0, 1, 0, 1)

    def delete_wallet(self, wallet_id, *_):
        try:
            with db.atomic():
                Wallet.get_by_id(wallet_id).delete_instance(recursive=True)  # удалит и WalletMoney связанные
            self.build_table()
        except Exception as e:
            self.show_error(f"Deletion error: {e}")

    def show_wallet_money_popup(self, wallet, *_):
        # Переходим к редактированию/просмотру купюр для выбранного кошелька
        popup = Popup(title=f'Wallet #{wallet.id} Bills', size_hint=(0.9, 0.9))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Таблица купюр
        scroll = ScrollView()
        grid = GridLayout(cols=5, size_hint_y=None, spacing=5)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['Denomination', 'Type', 'Quantity', 'Edit', 'Delete']
        for title in headers:
            grid.add_widget(Label(text=f'[b]{title}[/b]', markup=True, size_hint_y=None, height=30))

        for wm in WalletMoney.select().where(WalletMoney.wallet == wallet):
            grid.add_widget(Label(text=str(wm.money.money_nominal)))
            grid.add_widget(Label(text=str(wm.money.types)))
            grid.add_widget(Label(text=str(wm.quantity)))

            btn_edit = Button(text='✏️', size_hint_y=None, height=30)
            btn_edit.bind(on_press=partial(self.show_edit_wallet_money_popup, wm))
            grid.add_widget(btn_edit)

            btn_del = Button(text='🗑️', size_hint_y=None, height=30)
            btn_del.bind(on_press=partial(self.delete_wallet_money, wm.id))
            grid.add_widget(btn_del)

        scroll.add_widget(grid)
        layout.add_widget(scroll)

        btn_add = Button(text='Add Bill', size_hint_y=None, height=40)
        btn_add.bind(on_press=lambda *_: self.show_add_wallet_money_popup(wallet))
        layout.add_widget(btn_add)

        popup.content = layout
        popup.open()

    def show_add_wallet_money_popup(self, wallet):
        popup = Popup(title='Add Bill to Wallet', size_hint=(0.8, 0.8))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        money_scroll = ScrollView(size_hint=(1, None), height=200)
        money_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        money_list.bind(minimum_height=money_list.setter('height'))

        self.money_btns = []
        for money in Money.select():
            btn = Button(text=f"{money.money_nominal} ({money.types})", size_hint_y=None, height=40)
            btn.money = money
            self.money_btns.append(btn)
            money_list.add_widget(btn)
        money_scroll.add_widget(money_list)

        layout.add_widget(Label(text="Select Denomination:"))
        layout.add_widget(money_scroll)

        quantity_box = BoxLayout(size_hint_y=None, height=40)
        quantity_box.add_widget(Label(text="Quantity:"))
        inp_quantity = TextInput(input_filter='int', text='1')
        quantity_box.add_widget(inp_quantity)
        layout.add_widget(quantity_box)

        btn_save = Button(text='Save', size_hint_y=None, height=40)
        layout.add_widget(btn_save)

        self.selected_money = None

        for btn in self.money_btns:
            btn.bind(on_press=self.select_money)

        popup.content = layout
        popup.open()

        def save_bill(instance):
            try:
                if not self.selected_money:
                    raise ValueError("Denomination not selected")
                quantity = int(inp_quantity.text)
                if quantity <= 0:
                    raise ValueError("Quantity must be positive")

                with db.atomic():
                    wm, created = WalletMoney.get_or_create(wallet=wallet, money=self.selected_money, defaults={'quantity': 0})
                    wm.quantity += quantity
                    wm.save()
                popup.dismiss()
                self.show_wallet_money_popup(wallet)
            except Exception as e:
                self.show_error(str(e))

        btn_save.bind(on_press=save_bill)

    def show_edit_wallet_money_popup(self, wm, *_):
        popup = Popup(title='Edit Bill Quantity', size_hint=(0.6, 0.5))
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        quantity_box = BoxLayout(size_hint_y=None, height=40)
        quantity_box.add_widget(Label(text=f"Denomination: {wm.money.money_nominal} ({wm.money.types})"))
        layout.add_widget(quantity_box)

        quantity_box = BoxLayout(size_hint_y=None, height=40)
        quantity_box.add_widget(Label(text="Quantity:"))
        inp_quantity = TextInput(input_filter='int', text=str(wm.quantity))
        quantity_box.add_widget(inp_quantity)
        layout.add_widget(quantity_box)

        btn_save = Button(text='Save', size_hint_y=None, height=40)
        layout.add_widget(btn_save)

        popup.content = layout
        popup.open()

        def save_edit(instance):
            try:
                quantity = int(inp_quantity.text)
                if quantity < 0:
                    raise ValueError("Quantity cannot be negative")
                if quantity == 0:
                    wm.delete_instance()
                else:
                    wm.quantity = quantity
                    wm.save()
                popup.dismiss()
                self.show_wallet_money_popup(wm.wallet)
            except Exception as e:
                self.show_error(str(e))

        btn_save.bind(on_press=save_edit)

    def delete_wallet_money(self, wallet_money_id, *_):
        try:
            with db.atomic():
                WalletMoney.get_by_id(wallet_money_id).delete_instance()
            # Обновляем таблицу после удаления
            # Можно перерисовать popup или экран
            # Для простоты закроем и откроем заново popup с купюрами
            # Чтобы это сделать, надо знать wallet - можно получить из удаляемого объекта
            # Но объект уже удален, получим через try-except
            self.build_table()
        except Exception as e:
            self.show_error(f"Deletion error: {e}")

    def show_error(self, msg):
        Popup(title='Error',
              content=Label(text=msg),
              size_hint=(0.5, 0.3)).open()


class WalletCard(Screen):
    def on_pre_enter(self):
        self.build_table()

    def build_table(self):
        # Очистка предыдущего содержимого main_layout
        if hasattr(self, 'main_layout'):
            self.main_layout.clear_widgets()
        else:
            self.main_layout = BoxLayout(orientation='vertical', padding=10)
            self.add_widget(self.main_layout)

        main = self.main_layout
        # Верхняя панель с кнопками
        header = BoxLayout(size_hint_y=None, height=40, spacing=5)
        header.add_widget(Button(text='Back',
                                 on_press=lambda *_: setattr(self.manager, 'current', 'bank_dashboard')))
        header.add_widget(Button(text='Add Wallet',
                                 on_press=lambda *_: self.show_wallet_popup()))
        main.add_widget(header)

        # Таблица с прокруткой
        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        # Заголовки таблицы
        headers = ['Wallet ID', 'Card Number', 'Actions']
        for title in headers:
            grid.add_widget(Label(text=f'[b]{title}[/b]', markup=True,
                                  size_hint_y=None, height=30))

        # Заполнение строк таблицы
        for wallet in Wallet.select():
            grid.add_widget(Label(text=str(wallet.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=str(wallet.card.card_number), size_hint_y=None, height=30))

            actions = BoxLayout(spacing=5, size_hint_y=None, height=30)
            btn_edit = Button(text='✏️', size_hint_x=0.5)
            btn_edit.bind(on_press=lambda inst, wid=wallet.id: self.show_wallet_popup(wid))

            btn_del = Button(text='🗑️', size_hint_x=0.5)
            btn_del.bind(on_press=lambda inst, wid=wallet.id: self.delete_wallet(wid))

            actions.add_widget(btn_edit)
            actions.add_widget(btn_del)
            grid.add_widget(actions)

        scroll.add_widget(grid)
        main.add_widget(scroll)

    def show_wallet_popup(self, wallet_id=None, instance=None):
        """Окно добавления/редактирования кошелька"""
        is_edit = wallet_id is not None
        popup = Popup(
            title='Edit Wallet' if is_edit else 'Add Wallet',
            size_hint=(0.6, 0.5)
        )

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Выбор карты
        card_box = BoxLayout(orientation='vertical')
        card_box.add_widget(Label(text="Select Card:"))

        card_scroll = ScrollView(size_hint=(1, None), height=200)
        card_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        card_list.bind(minimum_height=card_list.setter('height'))
        self.card_buttons = []

        for card in CreditCards.select():
            btn = Button(text=f"{card.card_number} ({card.phone_field})", size_hint_y=None, height=40)
            btn.card = card
            self.card_buttons.append(btn)
            card_list.add_widget(btn)

        card_scroll.add_widget(card_list)
        card_box.add_widget(card_scroll)
        layout.add_widget(card_box)

        # Предварительное выделение выбранной карты (если редактируем)
        if is_edit:
            wallet = Wallet.get_by_id(wallet_id)
            self.selected_card = wallet.card
            for btn in self.card_buttons:
                if btn.card.id == self.selected_card.id:
                    btn.background_color = (0, 1, 0, 1)
        else:
            self.selected_card = None

        for btn in self.card_buttons:
            btn.bind(on_press=self.select_card)

        # Кнопка сохранения
        btn_save = Button(text="Save", size_hint_y=None, height=40)
        layout.add_widget(btn_save)

        popup.content = layout
        popup.open()

        def save_wallet(instance):
            try:
                if not self.selected_card:
                    raise ValueError("Card not selected")

                with db.atomic():
                    if is_edit:
                        wallet = Wallet.get_by_id(wallet_id)
                        wallet.card = self.selected_card
                        wallet.save()
                    else:
                        # Проверка на дубликаты
                        if Wallet.select().where(Wallet.card == self.selected_card).exists():
                            raise ValueError("Wallet with this card already exists")
                        Wallet.create(card=self.selected_card)

                popup.dismiss()
                self.build_table()
            except Exception as e:
                self.show_error(str(e))

        btn_save.bind(on_press=save_wallet)

    def select_card(self, instance):
        self.selected_card = instance.card
        for btn in self.card_buttons:
            btn.background_color = (1, 1, 1, 1)
        instance.background_color = (0, 1, 0, 1)

    def delete_wallet(self, wallet_id, *_):
        try:
            with db.atomic():
                Wallet.get_by_id(wallet_id).delete_instance()
            self.build_table()
        except Exception as e:
            self.show_error(f"Deletion error: {e}")

    def show_error(self, msg):
        Popup(title='Error', content=Label(text=msg),
              size_hint=(0.5, 0.3)).open()
