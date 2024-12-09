import requests
import dotenv
import os

dotenv.load_dotenv(override=True)

class MailAdmin:
    def __init__(self):
        self.url = os.getenv('MAIL_API_HOST')
        self.username = os.getenv('MAIL_ADMIN_USER')
        self.password = os.getenv('MAIL_ADMIN_PASS')
        if not self.url or not self.username or not self.password:
            raise ValueError("Mail API host, admin user and password must be set in .env")
    def create_user(self, email: str, password: str):
        response = requests.post(f"{self.url}/admin/mail/users/add", data={"email": email, "password": password}, auth=(self.username, self.password))
        print(response.text)
        return response.status_code == 200
      
    def delete_user(self, email: str):
        response = requests.post(f"{self.url}/admin/mail/users/remove", data={"email": email}, auth=(self.username, self.password))
        print(response.text)
        return response.status_code == 200
      
    def list_users(self):
        response = requests.get(f"{self.url}/admin/mail/users", auth=(self.username, self.password))
        return response.text
      
