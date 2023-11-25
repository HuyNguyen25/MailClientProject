from flet import*
import flet as ft
import LoginScreen
from time import *

def main(page:ft.Page):
    page.title="MAIL CLIENT"
    page.window_width=1320
    page.window_height=900
    page.add(LoginScreen.LoginScreen(page=page))
    

ft.app(target=main)