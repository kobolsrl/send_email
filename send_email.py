import smtplib
import imghdr
from email.message import EmailMessage
import datetime
import os
import json
import sys

msg = EmailMessage()
msg.set_charset('utf-8')
mails_sended=''
mails_to_send=''

email_bulk_file_exists = os.path.exists(f'email_bulk_list_sended_{datetime.datetime.now().date()}.txt')
json_file_exists = os.path.exists(f'config.json')

if not json_file_exists:
    config_file = {
        "author": "",
        "mails": "",
        "from": "",
        "password" : "",
        "body": "",
        "subject": "",
        "attachments": "[]"
    }
    json_object = json.dumps(config_file, indent = 7)

    with open("config.json", "w") as outfile:
        outfile.write(json_object)

    with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
        f.write('\n\n') 
        f.write(f'{os.getlogin()}'.center(100, '-'))
        f.write('\n') 
        f.write('Config file not found. A new one will be created.')
        sys.exit()

if email_bulk_file_exists:
    with open(f'email_bulk_list_sended_{datetime.datetime.now().date()}.txt', 'r') as a_file:
        mails_sended = a_file.read()
        
config_file = open('config.json')
config_file_as_json = json.load(config_file)

if not config_file_as_json['author']:
    author = os.getlogin()
else:
    author = config_file_as_json['author']
    
if not config_file_as_json['mails']:
    with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
        f.write('\n\n') 
        f.write(f'{author}'.center(100, '-'))
        f.write('\n') 
        f.write(f'You must add at least one mail to the config file')
        sys.exit()
        
if not config_file_as_json['from']:
    msg['From'] = 'info@grupokobol.com'
else:
    msg['From'] = f"{config_file_as_json['from']}"
 
if not config_file_as_json['password']:
    with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
        f.write('\n\n') 
        f.write(f'{author}'.center(100, '-'))
        f.write('\n') 
        f.write(f'You must add a mail and a password to the config file')
        sys.exit()

if not config_file_as_json['subject'] or not config_file_as_json['body']:
    with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
        f.write('\n\n') 
        f.write(f'{author}'.center(100, '-'))
        f.write('\n') 
        f.write(f'You must add a subject and a body to the config file')
        sys.exit()

msg['Subject'] = f"{config_file_as_json['subject']}"
msg.set_content(f"{config_file_as_json['body']}")

if config_file_as_json['attachments']:
    for attachment in config_file_as_json['attachments'].split(','):
        with open(attachment, 'rb') as f:
            file_data = f.read()
            file_type = imghdr.what(f.name)
            file_name = f.name
            msg.add_attachment(file_data, maintype='image', subtype=file_type, filename=file_name)
               
for mail in config_file_as_json['mails'].split(','):
    try:
        if email_bulk_file_exists:
            if(mail in mails_sended):
                continue
        
        if not msg['to']:
            msg.add_header('to', mail)
        else:
            msg.replace_header('to', mail)

        
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(config_file_as_json['from'], config_file_as_json['password'])
            
            try:
                smtp.send_message(msg)
                with open(f'email_bulk_list_sended_{datetime.datetime.now().date()}.txt', 'a') as f:
                    f.write('\n\n') 
                    f.write(f'{author}'.center(100, '-'))
                    f.write(f'\n {mail}|{datetime.datetime.now()}|status: success')
            except Exception as e:
                with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
                    f.write('\n\n') 
                    f.write(f'{author}'.center(100, '-'))
                    f.write('\n') 
                    f.write(f'{mail}|{datetime.datetime.now()}|status: error')
                    f.write('\n') 
                    f.write(f'{sys.exc_info()}')
                    f.write('\n')
                    f.write(f'{e}')
                
    except Exception as e:
        with open(f'error_{datetime.datetime.now().date()}.txt', 'a') as f:
            f.write('\n\n') 
            f.write(f'{author}'.center(100, '-'))
            f.write('\n') 
            f.write(f'{mail}|{datetime.datetime.now()}|status: error')
            f.write('\n') 
            f.write(f'{sys.exc_info()}')
            f.write('\n')
            f.write(f'{e}')
        
        

