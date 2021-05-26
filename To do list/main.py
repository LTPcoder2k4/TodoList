from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import OneLineListItem
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty

inp_helper = """
MDTextField:
    hint_text: "Name: "
    icon_right: "location-enter"
    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
    size_hint_x: None
    width: 700
"""


class ToDoListScreen(Screen):
    list_view = ObjectProperty(None)
    def addList(self):
        create_btn = MDFlatButton(text="Create", on_release=self.create_thing)
        close_btn = MDFlatButton(text="Close", on_release=self.close_inp)
        self.inpDialog = MDDialog(text="Create what to do", size_hint=(0.75, 1), buttons=[create_btn, close_btn])
        self.inp = Builder.load_string(inp_helper)
        self.inpDialog.add_widget(self.inp)
        self.inpDialog.open()

    def close_inp(self, obj):
        self.inpDialog.dismiss()

    def trim(self, txt):
        while len(txt) > 0:
            if txt[0] == ' ':
                txt = txt[1::]
            else:
                break
        while len(txt) > 0:
            if txt[-1] == ' ':
                txt = txt[:-1]
            else:
                break
        i = 0
        while i + 1 < len(txt):
            if txt[i] == txt[i + 1] == ' ':
                txt = txt[:i] + txt[i + 1:]
            else:
                i += 1
        return txt

    def create_thing(self, obj):
        self.inp.text = self.trim(self.inp.text)
        if self.inp.text == '':
            check_str = "Please enter a thing to do"
        else:
            check_str = "Create successful!"
            listTodo.append(self.inp.text)
            self.list_view.add_widget(OneLineListItem(text=self.inp.text, on_release=self.del_actDialog))
        close_btn = MDFlatButton(text="Close", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Creation", text=check_str, size_hint=(0.75, 1), buttons=[close_btn])
        self.dialog.open()

    def del_actDialog(self, obj):
        self.current_obj = obj
        yes_btn = MDFlatButton(text="Yes", on_release=self.del_act)
        no_btn = MDFlatButton(text="No", on_release=self.close_actDialog)
        self.actDialog = MDDialog(title="Delete activity", text="Have you finished this activity?", size_hint=(0.75, 1), buttons=[yes_btn, no_btn])
        self.actDialog.open()

    def del_act(self, obj):
        self.list_view.remove_widget(self.current_obj)
        listTodo.remove(self.current_obj.text)
        self.close_actDialog(obj)

    def close_actDialog(self, obj):
        self.actDialog.dismiss()

    def close_dialog(self, obj):
        self.dialog.dismiss()
        if self.inp.text != '':
            self.close_inp(obj)


class ToDoListApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Pink"
        return ToDoListScreen()

    def on_start(self):
        try:
            with open("db.inp", 'r') as f:
                temp = f.read().splitlines()
                for i in temp:
                    listTodo.append(u'{}'.format(i))
        except:
            f = open("db.inp", 'w')
            f.close()
        for i in listTodo:
            self.root.ids.list_view.add_widget(OneLineListItem(text=i, on_release=self.del_actDialog))

    def del_actDialog(self, obj):
        self.current_obj = obj
        yes_btn = MDFlatButton(text="Yes", on_release=self.del_act)
        no_btn = MDFlatButton(text="No", on_release=self.close_dialog)
        self.dialog = MDDialog(title="Delete activity", text="Have you finished this activity?", size_hint=(0.75, 1), buttons=[yes_btn, no_btn])
        self.dialog.open()

    def del_act(self, obj):
        self.root.ids.list_view.remove_widget(self.current_obj)
        listTodo.remove(self.current_obj.text)
        self.close_dialog(obj)

    def close_dialog(self, obj):
        self.dialog.dismiss()

    def on_stop(self):
        with open("db.inp", 'w') as f:
            for i in listTodo:
                f.write(u'{}\n'.format(i))


listTodo = []
ToDoListApp().run()
