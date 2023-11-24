import flet as ft
from flet import *
import Email
import json
import LoginScreen

filePaths=[]
fileNames=[]
sender=''
def load_sender():
    global sender
    f=open('res/configurations/login_info.json')
    sender=json.load(f)['email']

def send_email_screen(page: ft.Page):
    page.window_height = 900
    page.window_width = 1280
    page.title="MAIN SCREEN"
    page.scroll=True

    #logo
    email_logo=Image(
        src=f"res/icons/email_logo.png",
        width=80,
        height=80,
        fit=ft.ImageFit.CONTAIN,
    )

    def exit(e):
        page.controls.pop()
        LoginScreen.login_screen(page=page)

    #popup menu
    popup_menu=ft.PopupMenuButton(
        icon=ft.Icon(name=ft.icons.MENU),
        items=[
            ft.PopupMenuItem(
                text="Inbox",
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
                text="Exit",
                on_click=exit
            )
        ]
    )

    header_row=Row(
        alignment=MainAxisAlignment.SPACE_BETWEEN,
        controls=[
            email_logo,
            popup_menu
        ]
    )

    load_sender()
    txt_sender=ft.TextField(label="From: ",hint_text="From", keyboard_type=KeyboardType.EMAIL,height=40)
    txt_sender.value=sender
    txt_sender.read_only=True
    txt_receivers=ft.TextField(label="To: ",hint_text="To", keyboard_type=KeyboardType.EMAIL,height=40)
    txt_cc=ft.TextField(label="Cc:", hint_text="Cc", keyboard_type=KeyboardType.EMAIL,height=40)
    txt_bcc=ft.TextField(label="Bcc:", hint_text="Bcc", keyboard_type=KeyboardType.EMAIL,height=40)
    txt_subject=ft.TextField(label="Subject: ",hint_text="Subject",keyboard_type=KeyboardType.TEXT,height=40)
    txt_content=ft.TextField(label="Content: ",hint_text="Content",multiline=True,keyboard_type=KeyboardType.TEXT,min_lines=14)
   
    text_attachments=ft.Text(value="Attachments: "+', '.join(fileNames))
    
    def on_dialog_result(e):
        for file in e.files:
            filePaths.append(file.path)
            fileNames.append(file.name)
            text_attachments.value="Attachments: "+', '.join(fileNames)
        page.update()    

    file_picker=ft.FilePicker(on_result=on_dialog_result)
    page.overlay.append(file_picker)
    page.update()

    def attach_button_clicked(e):
        file_picker.pick_files(allow_multiple=True)

    btn_attach=ft.IconButton(
        icon=ft.icons.ATTACH_FILE,
        on_click=attach_button_clicked
    )

    def send_button_clicked(e):
        if txt_sender.value!='' and txt_receivers!='':
            email = Email.Email(
                sender=txt_sender.value,
                receivers=txt_receivers.value.split(', '),
                subject=txt_subject.value,
                message=txt_content.value,
                CC=txt_cc.value.split(', ') if txt_cc.value!='' else [],
                BCC=txt_bcc.value.split(', ') if txt_bcc.value!='' else [],
                attachments=filePaths
            )
            email.send_emails()

    btn_send=ft.IconButton(
        icon=ft.icons.SEND,
        icon_color="BLUE_500",
        icon_size=60,
        on_click=send_button_clicked
    ) 
    
    col=Column(
        #horizontal_alignment=CrossAxisAlignment.CENTER,
        alignment=MainAxisAlignment.START,
        controls=[
            header_row,
            txt_sender,
            txt_receivers,
            txt_cc,
            txt_bcc,
            txt_subject,
            ft.Row(
               alignment=MainAxisAlignment.END,
               controls=[
                   btn_attach
               ]
            ),
            ft.Row(
               controls=[
                   text_attachments
               ]
            ),
            txt_content,
            ft.Row(
                alignment=MainAxisAlignment.END,
                controls=[
                    btn_send
                ]
            )
        ]
    )
    page.add(col)

