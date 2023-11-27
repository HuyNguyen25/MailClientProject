import flet as ft
from flet import *
import Email
import json
import re

def load_sender():
    f=open('res/configurations/login_info.json')
    return json.load(f)['email']

class SendEmailScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page
        self.sender=load_sender()
        self.filePaths=[]
        self.fileNames=[]

    def build(self):
        self.txt_sender=ft.TextField(
            label="From: ",
            hint_text="From", 
            keyboard_type=KeyboardType.EMAIL,
            height=45,
            cursor_height=20
        )
        self.txt_sender.value=self.sender
        self.txt_sender.read_only=True
        self.txt_receivers=ft.TextField(
            label="To: ",
            hint_text="To", 
            keyboard_type=KeyboardType.EMAIL,
            height=45,
            cursor_height=20
        )
        self.txt_cc=ft.TextField(
            label="Cc:", 
            hint_text="Cc", 
            keyboard_type=KeyboardType.EMAIL,
            height=45,
            cursor_height=20
        )
        self.txt_bcc=ft.TextField(
            label="Bcc:", 
            hint_text="Bcc", 
            keyboard_type=KeyboardType.EMAIL,
            height=45,
            cursor_height=20
        )
        self.txt_subject=ft.TextField(
            label="Subject: ",
            hint_text="Subject",
            keyboard_type=KeyboardType.TEXT,
            height=45,
            cursor_height=20
        )
        self.txt_content=ft.TextField(
            label="Content: ",
            hint_text="Content",
            multiline=True,
            keyboard_type=KeyboardType.TEXT,
            min_lines=12
        )
    
        self.text_attachments=ft.Text(value="Attachments: "+', '.join(self.fileNames))
        
        def on_dialog_result(e):
            try:
                for file in e.files:
                    self.filePaths.append(file.path)
                    self.fileNames.append(file.name)
                    self.text_attachments.value="Attachments: "+', '.join(self.fileNames)
                self.update()
            except:
                pass    

        self.file_picker=ft.FilePicker(on_result=on_dialog_result)


        def attach_button_clicked(e):
            self.file_picker.pick_files(allow_multiple=True)

        self.btn_attach=ft.IconButton(
            icon=ft.icons.ATTACH_FILE,
            on_click=attach_button_clicked
        )

        def send_button_clicked(e):
            delimiters=',|;|/|&'
            space=' '
            if self.txt_sender.value!='' and self.txt_receivers!='':
                str_sender=self.txt_sender.value
                str_receivers=self.txt_receivers.value
                str_subject=self.txt_subject.value
                str_message=self.txt_content.value
                str_cc=self.txt_cc.value
                str_bcc=self.txt_bcc.value
                
                email = Email.Email(
                    sender=str_sender.strip(space),
                    receivers=[word.strip(space) for word in re.split(delimiters,str_receivers) if word.strip(space)],
                    subject=str_subject,
                    message=str_message,
                    CC=[word.strip(space) for word in re.split(delimiters,str_cc) if word.strip(space)],
                    BCC=[word.strip(space) for word in re.split(delimiters,str_bcc) if word.strip(space)],
                    attachments=self.filePaths
                )
                email.send_emails()

        self.btn_send=ft.IconButton(
            icon=ft.icons.SEND,
            icon_color="BLUE_500",
            icon_size=30,
            on_click=send_button_clicked
        ) 
        
        return ft.Column(
            #horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.START,
            controls=[
                self.file_picker,
                self.txt_sender,
                self.txt_receivers,
                self.txt_cc,
                self.txt_bcc,
                self.txt_subject,
                ft.Divider(
                   thickness=2,
                   color="BLACK" 
                ),
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


