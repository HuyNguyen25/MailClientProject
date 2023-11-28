import flet as ft
from flet import *
import json
import re

class SettingsScreen(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page=page
    
    def load_settings_data(self):
        f=open('res/configurations/filter_info.json')
        self.data=json.load(f)
    
    def build(self):
        self.load_settings_data()

        self.txt_project_filter=ft.TextField(
            label="Project",
            hint_text="Emails sent from these accounts will be moved to Project",
            multiline=True,
            prefix_icon="CONSTRUCTION_OUTLINED",
            value=', '.join(self.data['project'])
        )


        self.txt_important_filter=ft.TextField(
            label="Important",
            hint_text="Emails whose subjects contain these words will be moved to Important",
            multiline=True,
            prefix_icon="LABEL_IMPORTANT_OUTLINE",
            value=', '.join(self.data['important'])
        )
        
        self.txt_work_filter=ft.TextField(
            label="Work",
            hint_text="Emails whose contents contain these words will be moved to Work",
            multiline=True,
            prefix_icon="WORK_OUTLINE",
            value=', '.join(self.data['work'])
        )

        self.txt_spam_filter=ft.TextField(
            label="Spam",
            hint_text="Emails whose subjects or contents contain these words will be moved to Spam",
            multiline=True,
            prefix_icon="WARNING_AMBER_OUTLINED",
            value=', '.join(self.data['spam'])
        )

        def done_button_clicked(e):
            delimiters=',|;|/|&'
            space=' '
            project=self.txt_project_filter.value
            important=self.txt_important_filter.value
            work=self.txt_work_filter.value
            spam=self.txt_spam_filter.value

            project_items=[word.strip(space) for word in re.split(delimiters,project) if word.strip(space)]
            important_items=[word.strip(space) for word in re.split(delimiters,important) if word.strip(space)]
            work_items=[word.strip(space) for word in re.split(delimiters,work) if word.strip(space)]
            spam_items=[word.strip(space) for word in re.split(delimiters,spam) if word.strip(space)]
            
            self.data={
                "project":project_items,
                "important":important_items,
                "work":work_items,
                "spam":spam_items
            }
            json_object=json.dumps(self.data,indent=4)
            with open('res/configurations/filter_info.json','w') as json_file:
                json_file.write(json_object)

        self.btn_done=ft.TextButton(
            text="Done",
            width=80,
            height=60,
            on_click=done_button_clicked
        )

        return ft.Column(
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Emails sent from accounts in Project field will be moved to Project"
                ),
                ft.Text(
                    value="Emails whose subjects contain words in Important field will be moved to Important"
                ),
                ft.Text(
                    value="Emails whose contents contain words in Work field will be moved to Work"
                ),
                ft.Text(
                    value="Emails whose subjects or contents contain words in Spam will be moved to Spam"
                ),
                ft.Text(
                    value="Each items in the fields below is separated by , or ;"
                ),
                self.txt_project_filter,
                self.txt_important_filter,
                self.txt_work_filter,
                self.txt_spam_filter,
                self.btn_done
            ]
        )

