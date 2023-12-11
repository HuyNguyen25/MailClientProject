from email import message_from_bytes
import os.path
import re
import json
from socket import *
from math import *

class EmailPostOfficer:
    def __init__(self, account = '', time = ''):
        self.__account = account
        self.__refresh_time = time
        self.folders=[]
        
    def __get_number_of_mail(self, receive_message):
        message_split = receive_message.split()
        num = int(message_split[1])
        
        return num 
    
    def __get_retrieve_size(self, receive_message, index):
        list_split = receive_message.split()
        retrieveSize = []
        for i in range (1,len(list_split)):
            if i % 2 == 0:
                retrieveSize.append(list_split[i])
            
        return retrieveSize[index-1]
    
    def __get_boundary(self, receive_message):
        boundary_match = re.search(r'boundary="([^"]+)"', receive_message)
        
        if boundary_match:
            return boundary_match.group(1)

        return None
    
    def __get_body(self, mail_message):
        if mail_message.is_multipart():
            for part in mail_message.walk():
                if part.get_content_type() == 'text/plain':
                    payload_body = part.get_payload(decode=True).decode(part.get_content_charset())
                    message_body = payload_body.replace('\r\n','\n')
                    return message_body

        return ""
    
    def __get_attach_file_name(self, receive_message, folder):
        receive_mail = receive_message.encode()
        receive_content = receive_mail[(receive_mail.find("\r\n".encode())+2):]
        mail_message = message_from_bytes(receive_content)
        
        boundary = self.__get_boundary(receive_message)
        
        From = mail_message['From']
        
        list_file = []
        if mail_message.is_multipart():
            for part in mail_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    file_name = os.path.basename(part.get_filename()) 
                    full_path = os.path.join('res', 'emails', self.__account, folder, From, boundary, file_name)
                    list_file.append(full_path)
                    
        return list_file    
    
    def __receive_attach_file(self, receive_message):
        receive_mail = receive_message.encode()
        receive_content = receive_mail[(receive_mail.find("\r\n".encode())+2):]
        mail_message = message_from_bytes(receive_content)
        
        boundary = self.__get_boundary(receive_message)
        
        From = mail_message['From']
        
        if mail_message.is_multipart():
            for part in mail_message.walk():
                if part.get_content_type() == 'text/plain':
                    continue
                if part.get_content_type() == 'application/octet-stream':
                    file_name = os.path.basename(part.get_filename())

                    for folder in self.folders:
                        file_path = os.path.join('res', 'emails', self.__account, folder, From, boundary, file_name)
                        os.makedirs(os.path.dirname(file_path), exist_ok=True)                    
                        with open(file_path, 'wb') as file:
                            file.write(part.get_payload(decode = True))
    
    def __receive_content(self, receive_message):
        receive_mail = receive_message.encode()
        receive_content = receive_mail[(receive_mail.find("\r\n".encode())+2):]
        mail_message = message_from_bytes(receive_content)
        
        boundary = self.__get_boundary(receive_message)
        
        Date = mail_message['Date']
        From = mail_message['From']
        To = mail_message['To']
        Subject = mail_message['Subject']
        Cc = mail_message['Cc']
        Bcc = mail_message['Bcc']
        
        Body = self.__get_body(mail_message)
        
        Divider = '\n..................\n'

        if Bcc == None:
            mail_content = f'Date: {Date}\nFrom: {From}\nTo: {To}\nSubject: {Subject}\nCc: {Cc}{Divider}{Body}{Divider}'
        else:
            mail_content = f'Date: {Date}\nFrom: {From}\nTo: {To}\nSubject: {Subject}\nCc: {Cc}\nBcc: {Bcc}{Divider}{Body}{Divider}'

        structure_mail_content = {
            "Date" : Date,
            "From": From,
            "To":To,
            "Subject":Subject,
            "Cc":Cc,
            "Bcc":Bcc,
            "Body":Body
        }
        self.folders = self.__filter(structure_mail_content)
        
        for folder in self.folders:
            Attach_file_name = self.__get_attach_file_name(receive_message=receive_message,folder=folder)
            file_path = os.path.join('res', 'emails', self.__account, folder, From, boundary, 'content.txt')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                file.write(mail_content)
                for file_name in Attach_file_name:
                    file.write(f'{file_name}\n')
                              
        
    def receive_mail (self, pop3_server = '127.0.0.1', pop3_port = 3335):
        # Connect to POP3 server
        pop3_socket = socket(AF_INET, SOCK_STREAM)
        pop3_socket.connect((pop3_server, pop3_port))
    
        # Receive response from server
        response = pop3_socket.recv(1024).decode()
        
        # Send user name
        user_command = f'USER {self.__account}\r\n'
        pop3_socket.sendall(user_command.encode())
        response = pop3_socket.recv(1024).decode()
        
        # Send STAT
        stat_command = 'STAT\r\n'
        pop3_socket.sendall(stat_command.encode())
        response = pop3_socket.recv(1024).decode()
        num_message = self.__get_number_of_mail(response)
        
        # Send LIST to get Email list
        list_command = 'LIST\r\n'
        pop3_socket.sendall(list_command.encode())
        response = pop3_socket.recv(1024).decode()
        list_response = response
        
        # Send RETR to retrieve Email
        for i in range(1, num_message + 1):
            data=b""
            retrieve_command = f'RETR {i}\r\n'
            pop3_socket.sendall(retrieve_command.encode())
            retr_size = int(self.__get_retrieve_size(list_response, i))

            # Receive every segment of 1024 bytes
            for i in range(0,ceil(retr_size/1024)):
                data_segment=pop3_socket.recv(1024)
                if data_segment:
                    data+=data_segment
                if len(data_segment) < 1024:
                    break
            
            response=data.decode()
            
            self.__receive_content(receive_message=response)
            self.__receive_attach_file(receive_message=response)
            
        #Send DELE to delete message on server
        for i in range(1, num_message + 1):
            delete_command = f'DELE {i}\r\n'
            pop3_socket.sendall(delete_command.encode())
            response = pop3_socket.recv(1024).decode()
        
        # Disconnect
        quit_command = 'QUIT\r\n'
        pop3_socket.sendall(quit_command.encode())
        response = pop3_socket.recv(1024).decode()
        
        pop3_socket.close()

    def __filter(self, data):
        result = []
        name = 'res/configurations/filter_info.json'
        with open(name, 'r') as file:
            filter_config = json.load(file)
        for folder, vals in filter_config.items():
            for key, values in vals.items():

                if key == 'sender':
                    filter_data = data["From"]
                elif key == 'subject':
                    filter_data = data["Subject"]
                elif key == 'content':
                    filter_data = data["Body"]
                elif key == 'subject content':
                    filter_data = data["Subject"] + '\n' + data["Body"]

                filter_data = str(filter_data)
                if self.__filter_keyword(filter_data, values) and values:
                    result.append(folder) if key not in result else None
        file.close()
        if len(result)==0:
            result.append('inbox')
        return result

    def __filter_keyword(self, data, keywords):
        if not data: 
            return False
        pattern = re.compile('|'.join(r'\b'+re.escape(keyword) + r'\b'
                                      for keyword in keywords), flags=re.IGNORECASE)
        return pattern.search(data)