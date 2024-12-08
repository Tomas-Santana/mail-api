from flask import jsonify, Request
from middleware.validate_token import validate_token
from helpers.MailClient import MailClient
import ssl
from dotenv import load_dotenv
import os

load_dotenv()



def fetch_email(request: Request, inbox: str):
    jwtUser = validate_token(request)
    if not jwtUser:
        return jsonify({"error": "Invalid token"}), 401
    user_email = jwtUser.username + "@" + os.getenv("HOST_NAME", "")
    mail_client = MailClient(jwtUser.full_name, user_email, jwtUser.mail_password, ssl.create_default_context())
    messages = mail_client.fetch(inbox)
    return jsonify({
      "messages": [MailClient.mail_message_to_dict(message) for message in messages]
      }), 200

def mark_email(inbox: str, uid: str, request: Request):
    jwtUser = validate_token(request)
    if not jwtUser:
        return jsonify({"error": "Invalid token"}), 401
    user_email = jwtUser.username + "@" + os.getenv("HOST_NAME", "")
    mail_client = MailClient(jwtUser.full_name, user_email, jwtUser.mail_password, ssl.create_default_context())
    mail_client.mark_as_read(uid, inbox)
    
    return jsonify({"message": "Email marked as read"}), 200