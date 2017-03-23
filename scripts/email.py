import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from mimetypes import guess_type
from email.encoders import encode_base64
from smtplib import SMTP


class Email(object):
    def __init__(self, from_, to, subject, message, message_type='plain',
                 attachments=None, cc=None, message_encoding='us-ascii'):

        self.email = MIMEMultipart()
        self.email['From'] = from_
        self.email['To'] = to
        self.email['Subject'] = subject

        if cc is not None:
            self.email['Cc'] = cc
        text = MIMEText(message, message_type, message_encoding)
        self.email.attach(text)

        if attachments is not None:
            for filename in attachments:
                mimetype, encoding = guess_type(filename)
                mimetype = mimetype.split('/', 1)
                fp = open(filename, 'rb')
                attachment = MIMEBase(mimetype[0], mimetype[1])
                attachment.set_payload(fp.read())
                fp.close()
                encode_base64(attachment)
                attachment.add_header(
                    'Content-Disposition', 'attachment',
                    filename=os.path.basename(filename)
                )
                self.email.attach(attachment)

    def __str__(self):
        return self.email.as_string()


class EmailConnection(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connect()

    def connect(self):
        self.connection = SMTP('smtp.gmail.com', 587)
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()
        self.connection.login(self.username, self.password)

    def send(self, message, from_=None, to=None):
        if type(message) == str:
            if from_ is None or to is None:
                raise ValueError('You need to specify `from_` and `to`')
            else:
                from_ = from_
                to = to
        else:
            from_ = message.email['From']
            if 'Cc' not in message.email:
                message.email['Cc'] = ''
            to_emails = [message.email['To']] + message.email['Cc'].split(',')
            to = [complete_email for complete_email in to_emails]
            message = str(message)
        return self.connection.sendmail(from_, to, message)

    def close(self):
        self.connection.close()


from reporting.lib.email_tool import EmailConnection, Email
 

#user info
name = 'Rezwanul Islam'
email = 'your@email.com'
password = '******'

#receiver info
to_email = 'receiver@email.com'
to_name = 'Receiver Name'

subject = 'A nice email subject'
message = 'Message Body !'

attachments = []
 
print ('Connecting to server...')
server = EmailConnection(email, password)
print ('Preparing the email...')
email = Email(from_='"%s" <%s>' % (name, email),
              to='"%s" <%s>' % (to_name, to_email),
              subject=subject, message=message, attachments=attachments)
print ('Sending...')
server.send(email)
print ('Disconnecting...')
server.close()
print ('Done!')
