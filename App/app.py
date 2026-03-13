import os

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_mail import Mail, Message
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
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/contact/submit', methods=['POST'])
def contact_submit():
    fname   = request.form.get('fname', '').strip()
    lname   = request.form.get('lname', '').strip()
    name    = f"{fname} {lname}".strip() or request.form.get('name', '').strip()
    email   = request.form.get('email', '').strip()
    org     = request.form.get('org', '').strip()
    enquiry = request.form.get('enquiry', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not email or not message:
        flash('Please fill in all fields.', 'error')
        return redirect(url_for('contact'))

    # Send notification email to admin
    admin_html = load_email_template('contact_notification.html', {
        'name':    name,
        'email':   email,
        'org':     org,
        'enquiry': enquiry,
        'message': message
    })
    send_html_email(
        subject   = f'New Contact Form Submission from {name}',
        recipient = os.getenv('MAIL_DEFAULT_SENDER'),
        html_body = admin_html,
        text_body = f"Name: {name}\nEmail: {email}\nOrg: {org}\nEnquiry: {enquiry}\n\n{message}"
    )

    # Send confirmation email to the person who submitted
    confirm_html = load_email_template('contact_confirmation.html', {
        'name':    fname or name,
        'enquiry': enquiry,
        'message': message
    })
    send_html_email(
        subject   = 'We got your message – ShowWise',
        recipient = email,
        html_body = confirm_html,
        text_body = f"Hi {fname or name},\n\nThanks for reaching out! We'll be in touch within one business day.\n\nShowWise Team"
    )

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
    