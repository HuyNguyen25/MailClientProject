import flet as ft
from flet import *
import json
import re

class FilterSection(ft.UserControl):
    def __init__(self, filter_type: str, data: dict):
        super().__init__()
        self.filter_type=filter_type
        self.data=data

    def build(self):
        self.txt_sender_filter=ft.TextField(
            label="From: ",
            hint_text=f"Emails sent from these accounts will be moved to {self.filter_type.capitalize()}",
            multiline=True,
            filled=True,
            border=InputBorder.NONE,
            value=', '.join(self.data[self.filter_type]['sender'])
        )

        self.txt_subject_filter=ft.TextField(
            label="Subject has: ",
            hint_text=f"Emails with these words in their subjects will be moved to {self.filter_type.capitalize()}",
            multiline=True,
            filled=True,
            border=InputBorder.NONE,
            value=', '.join(self.data[self.filter_type]['subject'])
        )

        self.txt_content_filter=ft.TextField(
            label="Content has: ",
            hint_text=f"Emails with these words in their contents will be moved to {self.filter_type.capitalize()}",
            multiline=True,
            filled=True,
            border=InputBorder.NONE,
            value=', '.join(self.data[self.filter_type]['content'])
        )

        self.txt_subject_and_content_filter=ft.TextField(
            label="Has the words: ",
            hint_text=f"Emails with these words will be moved to {self.filter_type.capitalize()}",
            multiline=True,
            filled=True,
            border=InputBorder.NONE,
            value=', '.join(self.data[self.filter_type]['subject content'])
        )

        def done_button_clicked(e):
            delimiters=',|;|/|&|\n'
            space=' '
            senders=self.txt_sender_filter.value
            subjects=self.txt_subject_filter.value
            contents=self.txt_content_filter.value
            subjects_and_contents=self.txt_subject_and_content_filter.value

            sender_items=[word.strip(space) for word in re.split(delimiters,senders) if word.strip(space)]
            subject_items=[word.strip(space) for word in re.split(delimiters,subjects) if word.strip(space)]
            content_items=[word.strip(space) for word in re.split(delimiters,contents) if word.strip(space)]
            subject_and_content_items=[word.strip(space) for word in re.split(delimiters,subjects_and_contents) if word.strip(space)]

            filter_data={
                "sender": sender_items,
                "subject": subject_items,
                "content": content_items,
                "subject content": subject_and_content_items 
            }

            self.data[self.filter_type]=filter_data
            json_object=json.dumps(self.data,indent=4)
            with open('res/configurations/filter_info.json','w') as json_file:
                json_file.write(json_object)

        self.btn_done=ft.TextButton(
            text="Done",
            on_click=done_button_clicked
        )

        return ft.Column(
            controls=[
                ft.Text(
                    value=self.filter_type.capitalize()+' filter',
                    size=15
                ),
                self.txt_sender_filter,
                self.txt_subject_filter,
                self.txt_content_filter,
                self.txt_subject_and_content_filter,
                ft.Row(
                    alignment=MainAxisAlignment.END,
                    controls=[
                        self.btn_done
                    ]
                )
            ]
        )

class SettingsScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page=page
        f=open('res/configurations/filter_info.json')
        self.filter_data=json.load(f)
    
    def build(self):
        self.filter_settings=ft.Column(
            controls=[
                FilterSection(filter_type='project', data=self.filter_data),
                FilterSection(filter_type='important', data=self.filter_data),
                FilterSection(filter_type='work', data=self.filter_data),
                FilterSection(filter_type='spam', data=self.filter_data)
            ]
        )

        return ft.Column(
            controls=[
                ft.Text(
                    value='Filter settings',
                    size=20
                ),
                self.filter_settings
            ]
        )

