# send_email
A script that purpose is to send I emails

# How to use it
for use the script, i strongly recommend to create a folder in your local machine

there should be just a send_email.py file.

click on it and execute it, the first execution will trigger an error, this is normal, because this script
for work needs a config.json file the one that is going to be created after this first run.

now in your folder you should found the following files:
    send_email.py
    config.json

open config.jon with the editor of your preference.

it should be something likes this inside:
    {
        "author": "",
        *"mails": "",
        *"from": "",
        *"password": "",
        *"body": "",
        *"subject": "",
        "attachments": ""
    }
the fields mark with an asterisk are mandatory.

# fields dictionary
    
    -> mails: it should be a string, and here is where you defines emails that you want to send a mail.
        should looks like:
            mails: "example@example.com, example_2@example.com"
    -> from: it should be a string, and is here where you defines the email from you want to sen the emails.
        should looks like:
            from: "example@mail.com"
    -> password: it should be a string, and here is where you defines the password for the mail that you are using to send the mails.
        should looks like:
            password: "12356"
    -> body: it should be a string, and here is where you defines the content or body of the mail.
        should looks like:
            body: "my body test"
    -> subject: it should be a string, and here is where you defines the subject of the mail.
        should looks like:
            subject: "my subject test"