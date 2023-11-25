import flet as ft
from flet import *
import json
import MainScreen

def write_login_info(email='',password='',smtp_server='',smtp_port='',pop3_server='',pop3_port=''):
    data = {
        'email':email,
        'password':password,
        'smtp_server':smtp_server,
        'smtp_port':smtp_port,
        'pop3_server':pop3_server,
        'pop3_port':pop3_port,
    }
    json_object=json.dumps(data,indent=4)
    with open('res/configurations/login_info.json', 'w') as json_file:
        json_file.write(json_object)

def is_valid_login_info(email='',password='',smtp_server='',smtp_port='',pop3_server='',pop3_port=''):
    smtp_check = smtp_server=='127.0.0.1' and smtp_port=='2225'
    pop3_check = pop3_server=='127.0.0.1' and pop3_port=='3335'
    return email!=''and password!='' and smtp_check and pop3_check

class LoginScreen(ft.UserControl):   
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page
    def build(self):
        self.login_icon = ft.Image(
            src=f"res/icons/login.png",
            width=125,
            height=125,
            fit=ft.ImageFit.CONTAIN,
        )
        #Ui element
        self.txt_account=ft.TextField(
            label ="Email: ", 
            hint_text="Email Address", 
            keyboard_type=KeyboardType.EMAIL, 
            border=InputBorder.UNDERLINE
        )
        self.txt_password=ft.TextField(
            label="Password: ", 
            password = True, 
            can_reveal_password=True, 
            hint_text = "Password", 
            border=InputBorder.UNDERLINE
        )
        self.txt_smtp_server=ft.TextField(
            label="SMTP Sever: ",
            keyboard_type=KeyboardType.NUMBER
        )
        self.txt_smtp_server.value='127.0.0.1'
        self.txt_smtp_port=ft.TextField(
            label="SMTP Port: ",
            keyboard_type=KeyboardType.NUMBER
        )
        self.txt_smtp_port.value='2225'
        self.txt_pop3_server=ft.TextField(
            label="POP3 Sever: ",
            keyboard_type=KeyboardType.NUMBER
        )
        self.txt_pop3_server.value='127.0.0.1'
        self.txt_pop3_port=ft.TextField(
            label="POP3 Port: ",
            keyboard_type=KeyboardType.NUMBER
        )
        self.txt_pop3_port.value='3335'
        
        def btn_login_clicked(e):
            is_valid = is_valid_login_info(
                self.txt_account.value,
                self.txt_password.value,
                self.txt_smtp_server.value,
                self.txt_smtp_port.value,
                self.txt_pop3_server.value,
                self.txt_pop3_port.value
            )
            if is_valid:
                self.page.dialog=self.login_success_dlg
                self.login_success_dlg.open=True
                self.page.update()
            else:
                self.page.dialog=self.login_failed_dlg
                self.login_failed_dlg.open=True
                self.page.update()

        self.btn_login=ft.TextButton(
            text="Sign in",
            on_click=btn_login_clicked,
            width=100,
            height=60
        )    

        #dialog
        self.login_failed_dlg = ft.AlertDialog(
            title=ft.Text("Invalid login info, please login again!"),
            on_dismiss=lambda e: None
        )

        def go_to_main_screen(e):
            write_login_info(
                self.txt_account.value,
                self.txt_password.value,
                self.txt_smtp_server.value,
                self.txt_smtp_port.value,
                self.txt_pop3_server.value,
                self.txt_pop3_port.value
            )
            
            self.login_success_dlg.open=False
            self.page.update()
            self.page.controls.pop()
            self.page.add(MainScreen.MainScreen(page=self.page))

        self.login_success_dlg = ft.AlertDialog(
            title=ft.Text("Login successfully! Do you want to go to next page?"),
            actions=[
                ft.TextButton(text="OK",on_click=go_to_main_screen)
            ],
            on_dismiss=lambda e: None
        )

        def exit_button_clicked(e):
            self.page.window_destroy()

        self.btn_exit=ft.TextButton(
            text="Exit",
            on_click=exit_button_clicked,
            width=60,
            height=60
        )


        return ft.Column(
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            controls= [
                self.login_icon,
                self.txt_account,
                self.txt_password,
                self.txt_smtp_server,
                self.txt_smtp_port,
                self.txt_pop3_server,
                self.txt_pop3_port,
                ft.Row(
                    alignment=MainAxisAlignment.CENTER,
                    spacing=100,
                    controls=[
                        self.btn_login,
                        self.btn_exit
                    ]
                )
            ]
        )

