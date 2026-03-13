from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'true'),
    MAIL_USE_SSL=os.getenv('MAIL_USE_SSL', 'false'),
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
)

mail = Mail(app)

app.secret_key = os.getenv('SECRET_KEY')

mail = Mail(app)


                           