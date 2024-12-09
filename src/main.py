import logging
from controllers.auth.login import login, register
from controllers.mail.send_email import send_email
from controllers.mail.read_email import fetch_email, mark_email
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import os

load_dotenv(override=True)

print(os.getenv("HOST_NAME"))

app = Flask(__name__)
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5000"])

logging.getLogger('flask_cors').level = logging.DEBUG

@app.route("/auth/login", methods=["POST"])
def login_route():
    return login(request)

@app.route("/auth/register", methods=["POST"])
def register_route():
    return register(request)

@app.route("/mail/send", methods=["POST"])
def send_email_route():
    return send_email(request)

@app.route("/mail/fetch/<inbox>", methods=["GET"])
def fetch_email_route(inbox: str):
    return fetch_email(request, inbox)

@app.route("/mail/mark/<inbox>/<uid>", methods=["POST"])
def mark_email_route(inbox: str, uid: str):
    return mark_email(inbox, uid, request)



if __name__ == "__main__":
    app.run(debug=True)

