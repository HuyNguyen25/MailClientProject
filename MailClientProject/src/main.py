from flet import*
import flet as ft
import LoginScreen

def main(page:ft.Page):
    LoginScreen.login_screen(page)

ft.app(target=main)