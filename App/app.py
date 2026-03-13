import os

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

Emailtemplatesdir = os.path.join(os.path.dirname(__file__), 'email_templates')


#email helper functions 

def load_email_template(name: str, context: dict) -> str:
    """Load an HTML email template and substitute {{ key }} placeholders."""
    path = os.path.join(Emailtemplatesdir, name)
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()
    for key, value in context.items():
        html = html.replace('{{ ' + key + ' }}', str(value) if value else '')
        html = html.replace('{{' + key + '}}', str(value) if value else '')
    return html

def send_html_email(subject: str, recipient: str, html_body: str, text_body: str = ''):
    """Send an HTML email with an optional plain-text fallback."""
    msg = Message(subject, recipients=[recipient])
    msg.html = html_body
    if text_body:
        msg.body = text_body
    mail.send(msg)



#routs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    if not name or not email or not message:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('contact'))

    # Send email admin
    subject = f'New Contact Form Submission from {name}'
    recipient = os.getenv('MAIL_DEFAULT_SENDER')
    html_body = load_email_template('contact_notification.html', {
        'name': name,
        'email': email,
        'message': message
    })
    send_html_email(subject, recipient, html_body)

    flash('Your message has been sent successfully!', 'success')
    return redirect(url_for('contact'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn-more')
def learnmore():
    return render_template('learn-more.html')

if __name__ == '__main__':
    app.run(debug=True) 

