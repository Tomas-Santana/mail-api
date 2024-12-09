from flask import jsonify, Request, Response
from custom_types.api.login import LoginRequest
from custom_types.api.register import RegisterRequest
from custom_types.models.User import User
from helpers.token_funcs import get_token_from_user
from helpers.MailAdmin import MailAdmin
from dotenv import load_dotenv
import os

load_dotenv(override=True)
HOST_NAME = os.getenv("HOST_NAME", "")
if not HOST_NAME:
    raise ValueError("HOST_NAME must be set in .env")


def login(request: Request):
    try:
        login_request = LoginRequest.model_validate(request.json)
    except ValueError as e:
        return jsonify({"error": "invalid request"}), 400
    user = User.find_one({"username": login_request.username})
    if not user:
        return jsonify({"error": "User not found"}), 404
      
    if user.mail_password != login_request.password:
        return jsonify({"error": "Invalid password"}), 401
    
    token = get_token_from_user(user)
    user.mail_password = ""
    return jsonify({"token": token, "user": user.get_cleaned()}), 200

def register(request: Request):
    try:
        register_request = RegisterRequest.model_validate(request.json)
    except ValueError as e:
        return jsonify({"error": "invalid request"}), 400
    existing_user = User.find_one({"username": register_request.username})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400
    user = User.model_validate({
        "username": register_request.username,
        "mail_password": register_request.password,
        "full_name": register_request.full_name
    })
    user.save()
    mail_admin = MailAdmin()
    user_email = user.username + "@" + HOST_NAME
    success = mail_admin.create_user(user_email, user.mail_password)
    if not success:
        User.find_one_and_delete({"username": user.username})
        return jsonify({"error": "Failed to create user"}), 500
    token = get_token_from_user(user)
    user.mail_password = ""
    return jsonify({"token": token, "user": user.get_cleaned()}), 200

    

  