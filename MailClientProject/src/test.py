import flet as ft
from flet import *
import Email

class main_screen(ft.UserControl):
    def __init__(self):
        super().__init__()
        #logo
        self.email_logo=Image(
            src=f"res/icons/email_logo.png",
            width=80,
            height=80,
            fit=ft.ImageFit.CONTAIN,
        )
        
        #popup menu
        self.popup_menu=ft.PopupMenuButton(
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
                )
            ]
        )

        self.header_row=Row(
            alignment=MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                self.email_logo,
                self.popup_menu
            ]
        )

        self.txt_sender=ft.TextField(label="From: ",hint_text="From", keyboard_type=KeyboardType.EMAIL,height=40)
        self.txt_receivers=ft.TextField(label="To: ",hint_text="To", keyboard_type=KeyboardType.EMAIL,height=40)
        self.txt_cc=ft.TextField(label="Cc:", hint_text="Cc", keyboard_type=KeyboardType.EMAIL,height=40)
        self.txt_bcc=ft.TextField(label="Bcc:", hint_text="Bcc", keyboard_type=KeyboardType.EMAIL,height=40)
        self.txt_subject=ft.TextField(label="Subject: ",hint_text="Subject",keyboard_type=KeyboardType.TEXT,height=40)
        self.txt_content=ft.TextField(label="Content: ",hint_text="Content",multiline=True,keyboard_type=KeyboardType.TEXT,min_lines=14)
    

        self.filePaths=[]
        self.fileNames=[]
        self.text_attachments=ft.Text(value="Attachments: "+', '.join(self.fileNames))
        def on_dialog_result(e):
            for file in e.files:
                self.filePaths.append(file.path)
                self.fileNames.append(file.name)
                self.text_attachments.value="Attachments: "+', '.join(self.fileNames)
            self.controls.update()
            

        self.file_picker=ft.FilePicker(on_result=on_dialog_result)
        self.controls.append(self.file_picker)
        self.controls.update()

        def attach_button_clicked(e):
            self.file_picker.pick_files(allow_multiple=True)


        self.btn_attach=ft.IconButton(
            icon=ft.icons.ATTACH_FILE,
            on_click=attach_button_clicked
        )
        
        def send_button_clicked(e):
            if self.txt_sender.value!='' and self.txt_receivers!='':
                email = Email.Email(
                    sender=self.txt_sender.value,
                    receivers=self.txt_receivers.value.split(', '),
                    subject=self.txt_subject.value,
                    message=self.txt_content.value,
                    CC=self.txt_cc.value.split(', ') if self.txt_cc.value!='' else [],
                    BCC=self.txt_bcc.value.split(', ') if self.txt_bcc.value!='' else [],
                    attachments=self.sfilePaths
                )
                email.send_emails()

        self.btn_send=ft.IconButton(
            icon=ft.icons.SEND,
            icon_color="BLUE_500",
            icon_size=60,
            on_click=send_button_clicked
        )
    def build(self):
        col=Column(
            #horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.START,
            controls=[
                self.header_row,
                self.txt_sender,
                self.txt_receivers,
                self.txt_cc,
                self.txt_bcc,
                self.txt_subject,
                ft.Row(
                alignment=MainAxisAlignment.END,
                controls=[
                    self.btn_attach
                ]
                ),
                ft.Row(
                controls=[
                    self.text_attachments
                ]
                ),
                self.txt_content,
                ft.Row(
                    alignment=MainAxisAlignment.END,
                    controls=[
                        self.btn_send
                    ]
                )
            ]
        )
        return col

def main(page:ft.Page):
    page.add(main_screen())
ft.app(target=main)