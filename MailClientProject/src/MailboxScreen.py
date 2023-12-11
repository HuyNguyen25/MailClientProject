import flet as ft
from flet import *
import json 
import os
import EmailPostOfficer
import time
from threading import Thread

class MessageItem(ft.UserControl):
    def __init__(self, status='', path='', header='', content='', attachments='', del_func=None, seen_func=None):
        super().__init__()
        self.status=status
        self.path=path
        self.header=header
        self.content=content
        self.attachments=attachments
        self.del_func=del_func
        self.seen_func=seen_func
        
    def build(self):
        self.seen_icon=ft.Icon(
            name=ft.icons.MARK_EMAIL_READ if self.status == 'seen' else ft.icons.MARK_AS_UNREAD,
            color=ft.colors.RED_200 if self.status == 'unseen' else ft.colors.BLUE_200
        )
        self.txt_showing_item=ft.Text(
            value=self.header,
            selectable=True
        )
        def read_button_click(e):
            self.seen_func(self)
            self.txt_showing_item.value=self.header+'\n\n'+self.content+'\n\nAttachments: \n'+self.attachments
            self.update()

        def close_button_click(e):
            self.txt_showing_item.value=self.header
            self.update()

        def delete_button_click(e):
            self.del_func(self)

        return ft.Container(
            bgcolor="#E0E0E0",
            padding=ft.padding.all(10),
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=10,
                color=ft.colors.BLUE_GREY_500,
                offset=ft.Offset(0, 0),
                blur_style=ft.ShadowBlurStyle.NORMAL,
            ),
            border_radius=ft.border_radius.all(33),
            content=ft.Column(
                controls=[
                    self.seen_icon,
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
        
    

class MailboxScreen(ft.UserControl):
    def __init__(self, page:ft.Page, mail_box_folder='inbox'):
        super().__init__()
        self.page=page
        self.mail_box_folder=mail_box_folder
        with open('res/app_management/unseen_messages_info.json','r') as json_file:
            self.unseen_messages_data=json.load(json_file)

    def load_account_and_time_info(self):
       f=open('res/configurations/login_info.json')
       data=json.load(f)
       self.account=data['email']
       self.refreshing_time=data['autoload']

    def build(self):
        self.lv_message_list=ft.ListView(
            controls=[],
            expand=False,
            spacing=15
        )
        self.message_paths=[]
        def remove_empty_folders():
            folder_list=[]
            root_folder=os.path.join('res','emails',self.account)
            for foldername, subfolders, filenames in os.walk(root_folder): 
                folder_list.append(foldername)
                
            folder_list=reversed(folder_list)
            for folder in folder_list:
                if len(os.listdir(folder))==0:
                     os.rmdir(folder)

        def delete_message(del_mess: MessageItem):
            os.remove(del_mess.path)
            attachments=[attachment.strip() for attachment in del_mess.attachments.split('\n') if attachment.strip()!='']
            for item in attachments:
                os.remove(item)
            self.lv_message_list.controls.remove(del_mess)
            self.message_paths.remove(del_mess.path)

            if del_mess.path in self.unseen_messages_data[self.mail_box_folder]:
                self.unseen_messages_data[self.mail_box_folder].remove(del_mess.path)
                with open('res/app_management/unseen_messages_info.json','w') as json_file:
                    json_object=json.dumps(self.unseen_messages_data,indent=4)
                    json_file.write(json_object)

            remove_empty_folders()
            self.update()

        def seen_message(seen_mess: MessageItem):
            if seen_mess.status == 'unseen':
                seen_mess.status='seen'
                seen_mess.seen_icon.name=ft.icons.MARK_EMAIL_READ
                seen_mess.seen_icon.color=ft.colors.BLUE_200
                self.unseen_messages_data[self.mail_box_folder].remove(seen_mess.path)
                with open('res/app_management/unseen_messages_info.json','w') as json_file:
                    json_object=json.dumps(self.unseen_messages_data,indent=4)
                    json_file.write(json_object)

        def load_message_paths():
            self.message_paths.clear()
            root_folder=os.path.join('res','emails',self.account,self.mail_box_folder)
            for foldername, subfolders, filenames in os.walk(root_folder): 
                for filename in filenames:
                    if filename=='content.txt':
                        self.message_paths.append(os.path.join(foldername,filename))
        
        def load_message_items(): 
            Divider = '\n..................\n' 
            self.lv_message_list.controls.clear()
        
            for item in self.message_paths:
                with open(item,'r') as message_file:
                    header, content, attachments=message_file.read().split(Divider)
                
                    self.lv_message_list.controls.append(
                        MessageItem(
                            status='unseen' if item in self.unseen_messages_data[self.mail_box_folder] else 'seen',
                            path=item,
                            header=header,
                            content=content,
                            attachments=attachments,
                            del_func=delete_message,
                            seen_func=seen_message
                        )
                    )              

        self.load_account_and_time_info()
        load_message_paths()
        load_message_items()

        def retrieve_emails_button_clicked(e):
            EmailPostOfficer.EmailPostOfficer(account=self.account).receive_mail()
            with open('res/app_management/unseen_messages_info.json','r') as json_file:
                self.unseen_messages_data=json.load(json_file)
            load_message_paths()
            load_message_items()
            self.update()

        self.btn_retrieve_emails=ft.IconButton(
            icon="CLOUD_DOWNLOAD_OUTLINED",
            on_click=retrieve_emails_button_clicked,
        )

        # self.auto = True
        # def autoload():
        #     print("new thread")
        #     while True:
        #         self.btn_retrieve_emails.visible=False
        #         retrieve_emails_button_clicked(None)
        #         self.btn_retrieve_emails.visible=True
        #         time.sleep(2)

        # self.autoloadThread = Thread(target=autoload,args=(),daemon=True)
        # self.autoloadThread.start()
            
        return ft.Column(            
            controls=[
                ft.Row(
                    alignment=MainAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                value=self.mail_box_folder.capitalize(),
                                size=20,
                                color=ft.colors.BLACK
                            ),
                            bgcolor=ft.colors.GREY_300,
                            padding=16
                        )
                    ]
                ),
                ft.Row(
                    alignment=MainAxisAlignment.END,
                    controls=[
                        self.btn_retrieve_emails
                    ]
                ),
                self.lv_message_list           
            ]
        )
        