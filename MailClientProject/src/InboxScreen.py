import flet as ft
from flet import *
import json 
import os
import EmailPostOfficer

class MessageItem(ft.UserControl):
    def __init__(self, path='', header='', content='', attachments='', del_func=None):
        super().__init__()
        self.path=path
        self.header=header
        self.content=content
        self.attachments=attachments
        self.del_func=del_func
        
    def build(self):
        self.txt_showing_item=ft.Text(
            value=self.header
        )
        def read_button_click(e):
            self.txt_showing_item.value=self.header+'\n\n'+self.content+'\n\nAttachments: \n'+self.attachments
            self.update()

        def close_button_click(e):
            self.txt_showing_item.value=self.header
            self.update()

        def delete_button_click(e):
            self.del_func(self)

        return ft.Container(
            content=ft.Column(
                controls=[
                    self.txt_showing_item,
                    ft.Row(
                        controls=[
                            ft.TextButton(
                                text="Read",
                                on_click=read_button_click
                            ),
                            ft.TextButton(
                                text="Close",
                                on_click=close_button_click
                            ),
                            ft.TextButton(
                                text="Delete",
                                on_click=delete_button_click
                            )
                        ]
                    )
                ]
            )
        )
        
    

class InboxScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page

    def load_account_and_time_info(self):
       f=open('res/configurations/login_info.json')
       data=json.load(f)
       self.account=data['email']
       self.refreshing_time=data['autoload']

    def build(self):
        self.lv_message_list=ft.ListView(controls=[],expand=False,spacing=5)
        self.message_paths=[]
        def delete_message(del_mess):
            os.remove(del_mess.path)
            attachments=del_mess.attachments.split('\n')
            for item in attachments:
                os.remove(item)
            self.lv_message_list.controls.remove(del_mess)
            self.message_paths.remove(del_mess.path)
            self.update()

        def load_message_paths():
            self.message_paths.clear()
            for foldername, subfolders, filenames in os.walk(f'res\emails\{self.account}\inbox'): 
                for filename in filenames:
                    if filename=='content.txt':
                        self.message_paths.append(f'{foldername}\{filename}')
        
        def load_message_items():  
            self.lv_message_list.controls.clear()
        
            for item in self.message_paths:
                with open(item,'r') as message_file:
                    header,content,attachments=message_file.read().split('\n\n')
                    
                    self.lv_message_list.controls.append(
                        MessageItem(
                            path=item,
                            header=header,
                            content=content,
                            attachments=attachments,
                            del_func=delete_message
                        )
                    )
                    


        self.load_account_and_time_info()
        load_message_paths()
        load_message_items()

        def retrieve_emails_button_clicked(e):
            EmailPostOfficer.EmailPostOfficer(account=self.account).receive_mail()
            load_message_paths()
            load_message_items()
            self.update()

        self.btn_retrieve_emails=ft.IconButton(
            icon="CLOUD_DOWNLOAD_OUTLINED",
            on_click=retrieve_emails_button_clicked,
        )
        
        return ft.Column(
            controls=[
                ft.Row(
                    alignment=MainAxisAlignment.END,
                    controls=[
                        self.btn_retrieve_emails
                    ]
                ),
                self.lv_message_list           
            ]
        )
        