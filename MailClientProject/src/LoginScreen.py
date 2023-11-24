import flet as ft
from flet import *
import json
import SendEmailScreen

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

def login_screen(page: ft.Page):   
    page.window_height = 720
    page.window_width = 1280
    page.title  = "LOGIN"
    login_icon = ft.Image(
        src=f"res/icons/login.png",
        width=125,
        height=125,
        fit=ft.ImageFit.CONTAIN,
    )
    #Ui element
    txt_account = ft.TextField(label ="Email: ", hint_text="Email Address", keyboard_type=KeyboardType.EMAIL)
    txt_password = ft.TextField(label="Password: ", password = True, can_reveal_password=True, hint_text = "Password")
    txt_smtp_server = ft.TextField(label="SMTP Sever: ",keyboard_type=KeyboardType.NUMBER)
    txt_smtp_server.value='127.0.0.1'
    txt_smtp_port = ft.TextField(label="SMTP Port: ",keyboard_type=KeyboardType.NUMBER)
    txt_smtp_port.value='2225'
    txt_pop3_server = ft.TextField(label="POP3 Sever: ",keyboard_type=KeyboardType.NUMBER)
    txt_pop3_server.value='127.0.0.1'
    txt_pop3_port = ft.TextField(label="POP3 Port: ",keyboard_type=KeyboardType.NUMBER)
    txt_pop3_port.value='3335'
    
    def login_button_clicked(e):
        is_valid = is_valid_login_info(
            txt_account.value,
            txt_password.value,
            txt_smtp_server.value,
            txt_smtp_port.value,
            txt_pop3_server.value,
            txt_pop3_port.value
        )
        if is_valid:
            page.dialog=login_success_dlg
            login_success_dlg.open=True
            page.update()
        else:
            page.dialog=login_failed_dlg
            login_failed_dlg.open=True
            page.update()

    login_button = ft.TextButton(
        text="Login",
        on_click=login_button_clicked,
        width=100,
        height=100
    )    

    #dialog
    login_failed_dlg = ft.AlertDialog(
        title=ft.Text("Invalid login info, please login again!"),
        on_dismiss=lambda e: None
    )

    def go_to_main_screen(e):
        write_login_info(
            txt_account.value,
            txt_password.value,
            txt_smtp_server.value,
            txt_smtp_port.value,
            txt_pop3_server.value,
            txt_pop3_port.value
        )
        
        login_success_dlg.open=False
        page.update()
        page.controls.pop()
        SendEmailScreen.send_email_screen(page=page)

    login_success_dlg = ft.AlertDialog(
        title=ft.Text("Login successfully! Do you want to go to next page?"),
        actions=[
            ft.TextButton(text="OK",on_click=go_to_main_screen)
        ],
        on_dismiss=lambda e: None
    )

    col = ft.Column(
        horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.CENTER,
        controls= [login_icon,
        txt_account,
        txt_password,
        txt_smtp_server,
        txt_smtp_port,
        txt_pop3_server,
        txt_pop3_port,
        login_button]
    )

    page.add(col)
