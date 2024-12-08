from flask import jsonify, Request
from custom_types.api.send_email import SendEmailRequest
from helpers.MailClient import MailClient
from middleware.validate_token import validate_token
from dotenv import load_dotenv
import os
import ssl
load_dotenv()


def send_email(request: Request):
    jwtUser = validate_token(request)
    if not jwtUser:
        return jsonify({"error": "Invalid token"}), 401
    try:
        send_email_request = SendEmailRequest.model_validate(request.json)
    except ValueError as e:
        return jsonify({"error": "invalid request"}), 400
    user_email = jwtUser.username + "@" + os.getenv("HOST_NAME")
    mail_client = MailClient(jwtUser.full_name, user_email, jwtUser.mail_password, ssl.create_default_context())
    mail_client.send(send_email_request.email, send_email_request.subject, send_email_request.body)
    return jsonify({"message": "Email sent"}), 200