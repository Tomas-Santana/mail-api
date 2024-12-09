import imap_tools
import imaplib
import smtplib
import ssl
import dotenv
import os
import datetime
import email
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


dotenv.load_dotenv(override=True)

class MailClient:
    def __init__(self, full_name: str, email: str, password: str, context: ssl.SSLContext):
        self.host = os.getenv('HOST_NAME', "")
        print("host", self.host)
        self.smtp_port = int(os.getenv('SMTP_PORT', 465))
        self.imap_port = int(os.getenv('IMAP_PORT', 993))
        self.email = email
        self.full_name = full_name
        self.password = password
        self.context = context
        
        if not self.host or not self.smtp_port or not self.imap_port:
            raise ValueError("Host name, SMTP port and IMAP port must be set in .env")

    def send(self, to: list[str], subject: str, body: str, reply_to: str | None = None):
        message = MIMEMultipart()
        message["From"] = f"{self.full_name} <{self.email}>"
        message["To"] = ", ".join(to)
        message["Subject"] = subject
        message["Date"] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %z")
        if reply_to:
            message["Reply-To"] = reply_to
        message.attach(MIMEText(body, "plain"))
        
        text = message.as_string()
        with smtplib.SMTP_SSL(self.host, self.smtp_port, context=self.context) as server:
            server.login(self.email, self.password)
            server.sendmail(self.email, to, text)
            
        imap = imaplib.IMAP4_SSL(self.host, self.imap_port)
        imap.login(self.email, self.password)
        now = datetime.datetime.now(datetime.timezone.utc)
        imap.append("Sent", '\\Seen', imaplib.Time2Internaldate(now), text.encode())
        imap.logout()
        
        
            
    def fetch(self, inbox: str = "INBOX"):
        
        with imap_tools.mailbox.MailBox(self.host, self.imap_port).login(self.email, self.password, inbox) as mailbox: 
            for msg in mailbox.fetch():
                yield msg
                
    def mark_as_read(self, uid: str, inbox: str = "INBOX"):
        with imap_tools.mailbox.MailBox(self.host, self.imap_port).login(self.email, self.password, inbox) as mailbox:
            mailbox.flag(uid, imap_tools.consts.MailMessageFlags.SEEN, True)
    
    @staticmethod       
    def mail_message_to_dict(message: imap_tools.message.MailMessage):
        print(message.date, message.date_str)
        return {
            "uid": message.uid,
            "from": message.from_,
            "to": message.to,
            "subject": message.subject,
            "date": message.date,
            "text": message.text or "",
            "html": message.html or "",
            "flags": message.flags,
            "headers": message.headers
        }
    
    


