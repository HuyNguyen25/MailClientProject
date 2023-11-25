import flet as ft
from flet import*
import SendEmailScreen
import InboxScreen
import LoginScreen

class MainScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page
        self.screen_index=1
        self.option_container=ft.Container(
            content=SendEmailScreen.SendEmailScreen(page=page)
        )

    def build(self):
        #logo
        self.email_logo=Image(
            src=f"res/icons/email_logo.png",
            width=70,
            height=45,
            fit=ft.ImageFit.CONTAIN,
        )

        #pop up menu action
        def compose_email_clicked(e):
            if self.screen_index!=1:
                self.screen_index=1
                self.option_container.content=SendEmailScreen.SendEmailScreen(page=self.page)
                self.update()

        def inbox_clicked(e):
            if self.screen_index!=2:
                self.screen_index=2
                self.option_container.content=InboxScreen.InboxScreen(page=self.page)
                self.update()

        def exit_clicked(e):
            #self.page.controls.pop()
            self.page.controls.pop()
            self.page.add(LoginScreen.LoginScreen(page=self.page))
            

        #popup menu
        self.popup_menu=ft.PopupMenuButton(
            icon=ft.Icon(name=ft.icons.MENU),
            items=[
                ft.PopupMenuItem(
                    text="Compose Email",
                    on_click=compose_email_clicked
                ),
                ft.PopupMenuItem(
                    text="Inbox",
                    on_click=inbox_clicked
                ),
                ft.PopupMenuItem(
                    text="Project",
                ),
                ft.PopupMenuItem(
                    text="Important",
                ),
                ft.PopupMenuItem(
                    text="Work",
                ),
                ft.PopupMenuItem(
                    text="Spam",
                ),
                ft.PopupMenuItem(
                    text="Sign out",
                    on_click=exit_clicked
                )
            ]
        )

        self.header_row=ft.Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.email_logo,
                self.popup_menu
            ]
        )

        return ft.Column(
            alignment=CrossAxisAlignment.CENTER,
            controls=[
                self.header_row,
                self.option_container
            ]
        )
       