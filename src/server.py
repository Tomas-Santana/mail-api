from controllers.auth.login import login, register
from controllers.mail.send_email import send_email
from controllers.mail.read_email import read_email
from flask import Flask, request

app = Flask(__name__)

@app.route("/auth/login", methods=["POST"])
def login_route():
    return login(request)

@app.route("/auth/register", methods=["POST"])
def register_route():
    return register(request)

@app.route("/mail/send", methods=["POST"])
def send_email_route():
    return send_email(request)

@app.route("/mail/read", methods=["GET"])
def read_email_route():
    return read_email(request)

if __name__ == "__main__":
    app.run(debug=True)

