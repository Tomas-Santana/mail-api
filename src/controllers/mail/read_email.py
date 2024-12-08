from flask import jsonify, Request
from middleware.validate_token import validate_token
from helpers.MailClient import MailClient
import ssl
from dotenv import load_dotenv
import os
load_dotenv()

def read_email(request: Request):
    jwtUser = validate_token(request)
    if not jwtUser:
        return jsonify({"error": "Invalid token"}), 401
    user_email = jwtUser.username + "@" + os.getenv("HOST_NAME")
    mail_client = MailClient(jwtUser.full_name, user_email, jwtUser.mail_password, ssl.create_default_context())
    messages = mail_client.fetch()
    return jsonify({
      "messages": [MailClient.mail_message_to_dict(message) for message in messages]
      }), 200