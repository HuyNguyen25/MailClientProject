import flet as ft
from flet import *
import json 
import os
import EmailPostOfficer

class MessageItem():
    def __init__(self, path='', header='', content='', attachments=''):
        self.path=path
        self.header=header
        self.content=content
        self.attachments=attachments

class InboxScreen(ft.UserControl):
    def __init__(self, page:ft.Page):
        super().__init__()
        self.page=page

    def load_account_and_time_info(self):
       f=open('res/configurations/login_info.json')
       data=json.load(f)
       self.account=data['email']
       self.refreshing_time=data['autoload']

    def load_message_paths(self):
        self.message_paths=[]
        for foldername, subfolders, filenames in os.walk(f'res\emails\{self.account}\inbox'): 
            for filename in filenames:
                if filename=='content.txt':
                    self.message_paths.append(f'{foldername}\{filename}')
        
    def load_message_items(self):
        self.message_list=[]
        for item in self.message_paths:
            with open(item,'r') as message_file:
                header,content,attachments=message_file.read().split('\n\n')

                self.message_list.append(
                    MessageItem(
                        path=item,
                        header=header,
                        content=content,
                        attachments=attachments
                    )
                )


    def build(self):
        self.load_account_and_time_info()
        self.load_message_paths()
        self.load_message_items()

        def retrieve_emails_button_clicked(e):
            EmailPostOfficer.EmailPostOfficer(account=self.account).receive_mail()
            self.load_message_paths()
            self.load_message_items()
            update_inbox_list()
            self.update()

        self.btn_retrieve_emails=ft.IconButton(
            icon="CLOUD_DOWNLOAD_OUTLINED",
            on_click=retrieve_emails_button_clicked,
        )

        self.lv_inbox_list=ft.ListView(expand=False,spacing=5,width=500)
        self.txt_chosen_email=ft.Text(
            value=''
        )

        def update_inbox_list():
            self.lv_inbox_list.controls.clear()
            for item in self.message_list:

                title=ft.Text(
                    value=item.header
                )

                def read_button_clicked(e):
                    self.txt_chosen_email.value=item.header+'\n\n'+item.content+'\n\nAttachment paths: \n'+item.attachments
                    self.update()
                
                btn_read=ft.TextButton(
                    text="Read",
                    on_click=read_button_clicked
                )

                def close_button_clicked(e):
                    self.txt_chosen_email.value=''
                    self.update()
                
                btn_close=TextButton(
                    text="Close",
                    on_click=close_button_clicked
                )

                self.lv_inbox_list.controls.append(
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                title,
                                ft.Row(
                                    controls=[
                                        btn_read,
                                        btn_close
                                    ]
                                )
                            ]
                        )
                    )
                )
                                
        update_inbox_list()
        
        return ft.Column(
            controls=[
                ft.Row(
                    alignment=MainAxisAlignment.END,
                    controls=[
                        self.btn_retrieve_emails
                    ]
                ),
                ft.Row(
                   controls=[
                       self.lv_inbox_list,
                       ft.Divider(
                           thickness=1,
                           color="GRAY"
                       ),
                       ft.Column(
                            controls=[
                                self.txt_chosen_email
                            ]   
                       )                       
                   ]
                )
                
            ]
        )