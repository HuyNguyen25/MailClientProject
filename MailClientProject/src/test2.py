import os
def load_message_paths():
    message_paths=[]
    for foldername, subfolders, filenames in os.walk(f'res\emails\\2\inbox'): 
        for filename in filenames:
            if filename=='content.txt':
                print(f'{foldername}\{filename}')
                message_paths.append(f'{foldername}\{filename}')
    print(message_paths)

load_message_paths()    

