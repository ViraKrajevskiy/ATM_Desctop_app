from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout    import BoxLayout
from kivy.uix.gridlayout   import GridLayout
from kivy.uix.scrollview   import ScrollView
from kivy.uix.button       import Button
from kivy.uix.label        import Label
from kivy.uix.textinput    import TextInput
from kivy.uix.popup        import Popup
from kivy.uix.spinner      import Spinner

from Backend.data_base.core       import db
from Backend.ClassesNew.ATM.atm    import Atm
from Backend.ClassesNew.CASH.wallet import WalletMoney


class AtmManagementScreen(Screen):
    def on_pre_enter(self):
        self.build_screen()

    def build_screen(self):
        self.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # ─── Верхняя панель ───────────────────────────────────────────────────────
        top_bar = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_back = Button(text='Назад', size_hint_x=None, width=100)
        btn_back.bind(on_press=lambda *_: setattr(self.manager, 'current', 'bank_dashboard'))
        btn_add = Button(text='Добавить банкомат', size_hint_x=None, width=200)
        btn_add.bind(on_press=lambda *_: self.show_atm_popup())
        top_bar.add_widget(btn_back)
        top_bar.add_widget(btn_add)
        layout.add_widget(top_bar)
        # ──────────────────────────────────────────────────────────────────────────

        # ─── Таблица банкоматов ──────────────────────────────────────────────────
        self.build_atm_table(layout)
        # ──────────────────────────────────────────────────────────────────────────

        self.add_widget(layout)

    def build_atm_table(self, parent_layout):
        # Если уже есть старая таблица — удаляем
        if hasattr(self, 'table_container'):
            parent_layout.remove_widget(self.table_container)

        scroll = ScrollView()
        grid = GridLayout(cols=3, size_hint_y=None, spacing=5, padding=5)
        grid.bind(minimum_height=grid.setter('height'))

        # Заголовки
        for title in ['ID', 'Локация', 'Действия']:
            grid.add_widget(Label(text=f'[b]{title}[/b]', markup=True,
                                  size_hint_y=None, height=30))

        # Строки
        for atm in Atm.select():
            grid.add_widget(Label(text=str(atm.id),      size_hint_y=None, height=30))
            grid.add_widget(Label(text=atm.location,     size_hint_y=None, height=30))

            actions = BoxLayout(size_hint_y=None, height=30, spacing=5)
            btn_edit = Button(text='✏️', size_hint_x=0.5)
            btn_edit.bind(on_press=lambda inst, a=atm: self.show_atm_popup(a))
            btn_del = Button(text='🗑️', size_hint_x=0.5)
            btn_del.bind(on_press=lambda inst, a=atm: self.confirm_delete(a))
            actions.add_widget(btn_edit)
            actions.add_widget(btn_del)
            grid.add_widget(actions)

        scroll.add_widget(grid)
        self.table_container = scroll
        parent_layout.add_widget(scroll)

    def show_atm_popup(self, atm_instance=None):
        is_edit = atm_instance is not None
        popup = Popup(
            title='Редактировать банкомат' if is_edit else 'Добавить банкомат',
            size_hint=(0.8, 0.6)
        )

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        # — Локация
        inp_location = TextInput(
            hint_text='Локация банкомата',
            text=atm_instance.location if is_edit else '',
            multiline=False
        )
        layout.add_widget(Label(text='Локация:'))
        layout.add_widget(inp_location)

        # — Выбор записи WalletMoney (т. е. конкретного набора купюр в кошельке)
        #    Мы показываем список строк вида "WM-id: wallet_id ( denom×qty )"
        wm_records = list(WalletMoney.select())
        if not wm_records:
            popup.dismiss()
            return self.show_error_popup("Сначала создайте хотя бы один кошелёк с купюрами.")
        spinner_values = [
            f"{wm.id}: W{wm.wallet.id} [{wm.money.money_nominal}×{wm.quantity}]"
            for wm in wm_records
        ]
        spinner = Spinner(
            text=spinner_values[0] if is_edit else 'Выберите запись кошелька',
            values=spinner_values,
            size_hint_y=None,
            height=40
        )
        # если редактируем — установить текущее
        if is_edit:
            current = next((v for v in spinner_values if v.startswith(f"{atm_instance.wallet.id}:")), None)
            if current:
                spinner.text = current

        layout.add_widget(Label(text='Привязать к WalletMoney:'))
        layout.add_widget(spinner)

        btn_save = Button(text='Сохранить', size_hint_y=None, height=40)
        layout.add_widget(btn_save)

        popup.content = layout
        popup.open()

        def save_atm(inst):
            location = inp_location.text.strip()
            if not location:
                return self.show_error_popup("Локация не может быть пустой.")
            try:
                # Парсим id записи WalletMoney из спиннера
                wm_id = int(spinner.text.split(':', 1)[0])
                wm_obj = WalletMoney.get_by_id(wm_id)
                with db.atomic():
                    if is_edit:
                        atm_instance.location = location
                        atm_instance.wallet = wm_obj
                        atm_instance.save()
                    else:
                        Atm.create(location=location, wallet=wm_obj)
                popup.dismiss()
                self.build_screen()
            except Exception as e:
                self.show_error_popup(f"Ошибка сохранения: {e}")

        btn_save.bind(on_press=save_atm)

    def confirm_delete(self, atm_instance):
        popup = Popup(title='Подтверждение удаления', size_hint=(0.6, 0.4))
        box = BoxLayout(orientation='vertical', spacing=10, padding=10)
        box.add_widget(Label(text=f"Удалить банкомат #{atm_instance.id}?"))
        btns = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_yes = Button(text='Да'); btn_no = Button(text='Нет')
        btn_yes.bind(on_press=lambda *_: (popup.dismiss(), self.delete_atm(atm_instance)))
        btn_no .bind(on_press=lambda *_: popup.dismiss())
        btns.add_widget(btn_yes); btns.add_widget(btn_no)
        box.add_widget(btns)
        popup.content = box
        popup.open()

    def delete_atm(self, atm_instance):
        try:
            atm_instance.delete_instance()
            self.build_screen()
        except Exception as e:
            self.show_error_popup(f"Ошибка удаления: {e}")

    def show_error_popup(self, message):
        Popup(title='Ошибка', content=Label(text=message), size_hint=(0.5,0.3)).open()
        