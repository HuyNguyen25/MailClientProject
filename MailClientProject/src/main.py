from flet import *
import flet as ft
import LoginScreen
from time import *

  

def main(page:ft.Page):
    page.title="MAIL CLIENT"
    page.scroll=True
    page.theme_mode="light"
    page.add(LoginScreen.LoginScreen(page=page))


ft.app(target=main)
