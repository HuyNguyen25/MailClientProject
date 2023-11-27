import flet as ft
from flet import *

class InboxScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page

    def build(self):
        return Text("Inbox Screen")