from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from Backend.ClassesNew.ATM.atm import Atm
from Backend.data_base.core import db
from Backend.ClassesNew.CASH.wallet import Wallet

class AtmManagementScreen(Screen):
    def on_pre_enter(self):
        self.build_screen()

    def build_screen(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10)

        # Верхняя панель с кнопками
        top_bar = BoxLayout(size_hint_y=None, height=40)
        btn_back = Button(text='Назад')
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'bank_dashboard'))
        btn_add = Button(text='Добавить банкомат')
        btn_add.bind(on_press=lambda x: self.show_atm_popup())

        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_add)
        layout.add_widget(top_bar)

        # Таблица банкоматов
        self.build_atm_table(layout)
        self.add_widget(layout)

    def build_atm_table(self, layout):
        if hasattr(self, 'table_container'):
            layout.remove_widget(self.table_container)

        scroll_view = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ['ID', 'Локация', 'Действия']
        for h in headers:
            grid.add_widget(Label(text=f'[b]{h}[/b]', markup=True, size_hint_y=None, height=30))

        for atm in Atm.select():
            grid.add_widget(Label(text=str(atm.id), size_hint_y=None, height=30))
            grid.add_widget(Label(text=atm.location, size_hint_y=None, height=30))

            action_buttons = BoxLayout(size_hint_y=None, height=30)
            btn_edit = Button(text='✏️')
            btn_edit.bind(on_press=lambda x, a=atm: self.show_atm_popup(a))
            btn_delete = Button(text='🗑️')
            btn_delete.bind(on_press=lambda x, a=atm: self.confirm_delete(a))

            action_buttons.add_widget(btn_edit)
            action_buttons.add_widget(btn_delete)
            grid.add_widget(action_buttons)

        scroll_view.add_widget(grid)
        self.table_container = scroll_view
        layout.add_widget(scroll_view)

    def show_atm_popup(self, atm_instance=None):
        is_edit = atm_instance is not None
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        inp_location = TextInput(
            hint_text='Локация банкомата',
            text=atm_instance.location if is_edit else '')
        layout.add_widget(Label(text='Локация банкомата:'))
        layout.add_widget(inp_location)

        wallets = list(Wallet.select())
        wallet_choices = [f"{w.id} -" for w in wallets]
        spinner_wallet = Spinner(
            text='Выбери кошелёк',
            values=wallet_choices
        )

        if is_edit and atm_instance.wallet:
            try:
                selected_text = next(
                    f"{w.id} - {w.owner_name}" for w in wallets if w.id == atm_instance.wallet.id)
                spinner_wallet.text = selected_text
            except StopIteration:
                pass

        layout.add_widget(Label(text='Привязанный кошелёк:'))
        layout.add_widget(spinner_wallet)

        btn_save = Button(text='Сохранить')
        layout.add_widget(btn_save)

        popup = Popup(
            title='Редактировать банкомат' if is_edit else 'Добавить банкомат',
            content=layout,
            size_hint=(0.8, 0.6))
        popup.open()

        def save(instance):
            location = inp_location.text.strip()
            if not location:
                self.show_error_popup("Локация не может быть пустой")
                return

            if spinner_wallet.text == 'Выбери кошелёк':
                self.show_error_popup("Пожалуйста, выбери кошелёк")
                return

            try:
                wallet_id = int(spinner_wallet.text.split(' - ')[0])
                wallet = Wallet.get_by_id(wallet_id)

                with db.atomic():
                    if is_edit:
                        atm_instance.location = location
                        atm_instance.wallet = wallet
                        atm_instance.save()
                    else:
                        Atm.create(location=location, wallet=wallet)

                popup.dismiss()
                self.build_screen()
            except Exception as e:
                self.show_error_popup(f"Ошибка при сохранении: {e}")

        btn_save.bind(on_press=save)

    def confirm_delete(self, atm_instance):
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        layout.add_widget(Label(text=f"Удалить банкомат {atm_instance.location}?"))

        button_box = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_yes = Button(text='Да')
        btn_no = Button(text='Нет')
        button_box.add_widget(btn_yes)
        button_box.add_widget(btn_no)
        layout.add_widget(button_box)

        popup = Popup(title='Подтверждение', content=layout, size_hint=(0.6, 0.3))
        popup.open()

        btn_no.bind(on_press=popup.dismiss)
        btn_yes.bind(on_press=lambda x: (popup.dismiss(), self.delete_atm(atm_instance)))

    def delete_atm(self, atm_instance):
        try:
            atm_instance.delete_instance()
            self.build_screen()
        except Exception as e:
            self.show_error_popup(f"Ошибка при удалении: {e}")

    def show_error_popup(self, message):
        popup = Popup(title='Ошибка', content=Label(text=message), size_hint=(0.5, 0.3))
        popup.open()
