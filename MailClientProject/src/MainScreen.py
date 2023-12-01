import flet as ft
from flet import*
import SendEmailScreen
import MailboxScreen
import LoginScreen
import SettingsScreen

class MainScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page
        self.page.bgcolor=ft.colors.WHITE
        self.screen_index=1
        self.option_container=ft.Container(
            content=SendEmailScreen.SendEmailScreen(page=self.page)
        )

    def build(self):
        self.page.bgcolor="GREY_100"
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
                self.option_container.content=MailboxScreen.MailboxScreen(page=self.page, mail_box_folder='inbox')
                self.update()

        def project_clicked(e):
            if self.screen_index!=3:
                self.screen_index=3
                self.option_container.content=MailboxScreen.MailboxScreen(page=self.page,mail_box_folder='project')
                self.update()

        def important_clicked(e):
            if self.screen_index!=4:
                self.screen_index=4
                self.option_container.content=MailboxScreen.MailboxScreen(page=self.page,mail_box_folder='important')
                self.update()

        def work_clicked(e):
            if self.screen_index!=5:
                self.screen_index=5
                self.option_container.content=MailboxScreen.MailboxScreen(page=self.page,mail_box_folder='work')
                self.update()

        def spam_clicked(e):
            if self.screen_index!=6:
                self.screen_index=6
                self.option_container.content=MailboxScreen.MailboxScreen(page=self.page,mail_box_folder='spam')
                self.update()        

        def settings_clicked(e):
            if(self.screen_index!=7):
                self.screen_index=7
                self.option_container.content=SettingsScreen.SettingsScreen(page=self.page)
                self.update()
        
        def exit_clicked(e):
            #self.page.controls.pop()
            self.page.controls.pop()
            self.page.add(LoginScreen.LoginScreen(page=self.page))
            

        #popup menu
        self.popup_menu=ft.PopupMenuButton(
            icon="MENU",
            items=[
                ft.PopupMenuItem(
                    text="Compose Email",
                    icon = "CREATE_OUTLINED",
                    on_click=compose_email_clicked
                ),
                ft.PopupMenuItem(
                    text="Inbox",
                    icon="ALL_INBOX_OUTLINED",
                    on_click=inbox_clicked
                ),
                ft.PopupMenuItem(
                    text="Project",
                    icon="CONSTRUCTION_OUTLINED",
                    on_click=project_clicked
                ),
                ft.PopupMenuItem(
                    text="Important",
                    icon="LABEL_IMPORTANT_OUTLINE",
                    on_click=important_clicked
                ),
                ft.PopupMenuItem(
                    text="Work",
                    icon="WORK_OUTLINE",
                    on_click=work_clicked
                ),
                ft.PopupMenuItem(
                    text="Spam",
                    icon="WARNING_AMBER_OUTLINED",
                    on_click=spam_clicked
                ),
                ft.PopupMenuItem(
                    text="Settings",
                    icon="SETTINGS_OUTLINED",
                    on_click=settings_clicked
                ),
                ft.PopupMenuItem(
                    text="Sign out",
                    icon="LOGOUT",
                    on_click=exit_clicked
                )
            ]
        )

        header_row=ft.Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.email_logo,
                self.popup_menu
            ]
        )

        return ft.Column(
            alignment=CrossAxisAlignment.CENTER,
            controls=[
                header_row,
                self.option_container
            ]
        )
       