# -*- coding: utf-8 -*-
# Project: sendvar2mail
# File: emailsend.py
# Author: Andrey V. Baldin
# Mail: a.baldin@nsu.ru
# Year: 2020

import smtplib                                              
import os                                                   
import mimetypes                                            
from email import encoders                                  
from email.mime.base import MIMEBase                        
from email.mime.text import MIMEText                        
from email.mime.image import MIMEImage                      
from email.mime.audio import MIMEAudio                      
from email.mime.multipart import MIMEMultipart
from config import FROM_ADDR, LOGIN, PASSWORD, SUBJECT, TEXT, PATH

 
def send_email(addr_to, msg_subj, msg_text, files):
                                  
    msg = MIMEMultipart()                                   
    msg['From']    = FROM_ADDR                              
    msg['To']      = addr_to                                
    msg['Subject'] = msg_subj                               
    body = msg_text                                         
    msg.attach(MIMEText(body, 'plain'))                     
    process_attachement(msg, files)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(LOGIN, PASSWORD)
    server.sendmail(FROM_ADDR, addr_to, msg.as_string())
    server.quit()
    print("Отправка пользователю {0} завершена".format(addr_to))
 
def process_attachement(msg, files):                        
    print('proc attachment:',msg)
    for f in files:
        if os.path.isfile(f): 
            print('файл {0} существует'.format(f))                              
            attach_file(msg,f)                                     
            

def attach_file(msg, filepath):                             
    filename = os.path.basename(filepath)                                                          
    with open(filepath, 'rb') as fp:
        file = MIMEBase('application', "octet-stream")              
        file.set_payload(fp.read())                     
        fp.close()
        encoders.encode_base64(file)                    
    file.add_header('Content-Disposition', 'attachment', filename=filename) 
    msg.attach(file)                                        
    print("Файл {0} прикреплен".format(filename))
 

def parse_txt(file):
    with open('mail.txt') as f:
        input_data = list(f)
        for f in input_data:
            email = f.rsplit(':')[0] 
            variant = f.split(':')[1]
            variant = ' '.join(variant.split())
            variant = list(variant.split(','))
            main(email, variant)
        
        
def main(email,variant):
    files = []
    for f in variant:
        path = '{0}{1}.pdf'.format(PATH,f)
        files.append(path)
    send_email(email, SUBJECT, TEXT, files)


file = "mail.txt"
parse_txt(file)
