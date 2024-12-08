import imap_tools
import smtplib
import ssl
import dotenv
import os

dotenv.load_dotenv()

class MailClient:
    def __init__(self, full_name: str, email: str, password: str, context: ssl.SSLContext):
        self.host = os.getenv('HOST_NAME', "")
        self.smtp_port = os.getenv('SMTP_PORT', 465)
        self.imap_port = os.getenv('IMAP_PORT', 993)
        self.email = email
        self.full_name = full_name
        self.password = password
        self.context = context
        
        if not self.host or not self.smtp_port or not self.imap_port:
            raise ValueError("Host name, SMTP port and IMAP port must be set in .env")

    def send(self, to: str, subject: str, body: str):
        message = f"""From: {self.full_name} <{self.email}>
To: {to}
Subject: {subject}

{body}
"""

        with smtplib.SMTP_SSL(self.host, self.smtp_port, self.context) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, to, message)
            
    def fetch(self, inbox: str = "INBOX"):
        with imap_tools.MailBox(self.host, self.imap_port).login(self.email, self.password, inbox) as mailbox: 
            for msg in mailbox.fetch():
                yield msg

    def fetch_unread(self, inbox: str = "INBOX"):
        with imap_tools.MailBox(self.host, self.imap_port).login(self.email, self.password, inbox) as mailbox:
            for msg in mailbox.fetch('(UNSEEN)'):
                yield msg
                
    def mail_message_to_dict(message: imap_tools.message.MailMessage):
        return {
            "from": message.from_,
            "to": message.to,
            "subject": message.subject,
            "date": message.date,
            "text": message.text or "",
            "html": message.html or ""
        }
    


