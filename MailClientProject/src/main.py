from flet import *
import flet as ft
import LoginScreen
from time import *


def main(page: ft.Page):
    page.title = "MAIL CLIENT"
    page.scroll = True
    # page.theme=ft.Theme(
    #     color_scheme=ft.ColorScheme(
    #         primary =  "0xFF006496",
    #         on_primary =  '0xFFFFFFFF',
    #         primary_container = '0xFFCCE5FF',
    #         on_primary_container =  '0xFF001E31',
    #         secondary =  '0xFF50606F',
    #         on_secondary =  '0xFFFFFFFF',
    #         secondary_container =  '0xFFD4E4F6',
    #         on_secondary_container =  '0xFF0D1D2A',
    #         tertiary =  '0xFF66587B',
    #         on_tertiary =  '0xFFFFFFFF',
    #         tertiary_container =  '0xFFECDCFF',
    #         on_tertiary_container =  '0xFF211534',
    #         error =  '0xFFBA1A1A',
    #         error_container =  '0xFFFFDAD6',
    #         on_error =  '0xFFFFFFFF',
    #         on_error_container =  '0xFF410002',
    #         background =  '0xFFFCFCFF',
    #         on_background =  '0xFF1A1C1E',
    #         surface =  '0xFFFCFCFF',
    #         on_surface =  '0xFF1A1C1E',
    #         surface_variant =  '0xFFDEE3EB',
    #         on_surface_variant =  '0xFF42474E',
    #         outline =  '0xFF72787E',
    #         on_inverse_surface =  '0xFFF0F0F4',
    #         inverse_surface =  '0xFF2F3133',
    #         inverse_primary =  '0xFF91CDFF',
    #         shadow =  "0xFF000000",
    #         surface_tint =  '0xFF006496',
    #         outline_variant =  '0xFFC2C7CE',
    #         scrim =  '0xFF000000'
    #     )
    # )
    page.add(LoginScreen.LoginScreen(page=page))


ft.app(target=main)
