from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from socket import *

class Email():
    def __init__(self, sender = '', receivers = [], subject = '', message = '', CC = [], BCC = '', attachments = []):
        self.__sender = sender
        self.__receivers = receivers 
        self.__subject = subject
        self.__message = message
        
        self.__CC = CC
        self.__BCC = BCC
        self.__attachments = attachments
        
    def __send_cc_emails(self, smtp_server = '127.0.0.1', smtp_port = 2225):
        # Connect to SMTP server
        smtp_socket = socket(AF_INET, SOCK_STREAM)
        smtp_socket.connect((smtp_server, smtp_port))
    
        # Receive response from server
        response = smtp_socket.recv(1024).decode()
    
        # Send EHLO to start a session
        ehlo_command = 'EHLO MailServer\r\n'
        smtp_socket.sendall(ehlo_command.encode())
        response = smtp_socket.recv(1024).decode()
    
        # Send MAIL FROM and RCPT TO
        mail_from_command = f'MAIL FROM: <{self.__sender}>\r\n'
        smtp_socket.sendall(mail_from_command.encode())
        response = smtp_socket.recv(1024).decode()
    
        for rcv in self.__receivers:
            rcpt_to_command = f'RCPT TO: <{rcv}>\r\n'
            smtp_socket.sendall(rcpt_to_command.encode())
            response = smtp_socket.recv(1024).decode()

        for CC_rcv in self.__CC:
            rcpt_to_command = f'RCPT TO: <{CC_rcv}>\r\n'
            smtp_socket.sendall(rcpt_to_command.encode())
            response = smtp_socket.recv(1024).decode()
    
        # Send DATA to be able to enter the content of email
        data_command = 'DATA\r\n'
        smtp_socket.sendall(data_command.encode())
        response = smtp_socket.recv(1024).decode()
        
        # Create mime format mail
        email = MIMEMultipart()
        email['Date'] = datetime.now().strftime('%A, %d/%m/%Y, at %H:%M:%S')
        email['From'] = self.__sender
        email['To'] = ', '.join(self.__receivers)
        email['Subject'] = self.__subject
        email['Cc'] = ', '.join(self.__CC)   
        email.attach(MIMEText(self.__message, 'plain'))
        
        for attachment in self.__attachments:
            with open(attachment, 'rb') as file:
                part = MIMEApplication(file.read(), Name=attachment)
                part['Content-Disposition'] = f'attachment; filename="{attachment}"'
                email.attach(part)

        # Send content of email
        smtp_socket.sendall(email.as_string().encode())
        smtp_socket.sendall('\r\n.\r\n'.encode())
        response = smtp_socket.recv(1024).decode()
            
        # Disconnect
        quit_command = 'QUIT\r\n'
        smtp_socket.sendall(quit_command.encode())
        response = smtp_socket.recv(1024).decode()
    
        smtp_socket.close()               
            
    def __send_bcc_emails(self, smtp_server = '127.0.0.1', smtp_port = 2225):              
        for bcc_rcv in self.__BCC:
            #Create email
            email = MIMEMultipart()
            email['Date'] = datetime.now().strftime('%A, %d/%m/%Y, at %H:%M:%S')
            email['From'] = self.__sender
            email['To'] = ', '.join(self.__receivers)
            email['Subject'] = self.__subject
            email['Cc'] = ', '.join(self.__CC)   
            email.attach(MIMEText(self.__message, 'plain'))
        
            for attachment in self.__attachments:
                with open(attachment, 'rb') as file:
                   part = MIMEApplication(file.read(), Name=attachment)
                   part['Content-Disposition'] = f'attachment; filename="{attachment}"'
                   email.attach(part)
                
            email['Bcc'] = bcc_rcv
            # Connect to SMTP server
            smtp_socket = socket(AF_INET, SOCK_STREAM)
            smtp_socket.connect((smtp_server, smtp_port))
    
            # Receive response from server
            response = smtp_socket.recv(1024).decode()
    
            # Send EHLO to start a session
            ehlo_command = 'EHLO MailServer\r\n'
            smtp_socket.sendall(ehlo_command.encode())
            response = smtp_socket.recv(1024).decode()
    
            # Send MAIL FROM and RCPT TO
            mail_from_command = f'MAIL FROM: <{self.__sender}>\r\n'
            smtp_socket.sendall(mail_from_command.encode())
            response = smtp_socket.recv(1024).decode()
            
            rcpt_to_command = f'RCPT TO: <{bcc_rcv}>\r\n'
            smtp_socket.sendall(rcpt_to_command.encode())
            response = smtp_socket.recv(1024).decode()

            # Send DATA to be able to enter the content of email
            data_command = 'DATA\r\n'
            smtp_socket.sendall(data_command.encode())
            response = smtp_socket.recv(1024).decode()          
            
            # Send content of email
            smtp_socket.sendall(email.as_string().encode())
            smtp_socket.sendall('\r\n.\r\n'.encode())
            response = smtp_socket.recv(1024).decode()
            
            # Disconnect
            quit_command = 'QUIT\r\n'
            smtp_socket.sendall(quit_command.encode())
            response = smtp_socket.recv(1024).decode()
    
            smtp_socket.close()               

    def send_emails(self, smtp_server = '127.0.0.1', smtp_port = 2225):
        self.__send_cc_emails(smtp_server = smtp_server, smtp_port = smtp_port)
        self.__send_bcc_emails(smtp_server = smtp_server, smtp_port = smtp_port)

        
            
        




