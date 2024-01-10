from flask import Flask, render_template, request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        form_data = request.form

        # Process the form data (you may want to validate or sanitize it here)

        # Create an ASCII string from the form data
        ascii_data = '\n'.join([f'{key}: {value}' for key, value in form_data.items()])

        # Save the ASCII data to a file
        with open('form-data.txt', 'w') as file:
            file.write(ascii_data)

        # Send an email with the attached file
        send_email(ascii_data)

        # Stop the Flask development server
        sys.exit(0)

    except Exception as e:
        print(f"Error processing form: {e}")
        traceback.print_exc()  # Add this line to print the traceback
        return "Error processing form", 500

def send_email(ascii_data):
    # Configure email details for Hotmail (Outlook)
    sender_email = 'ci_320@hotmail.com'
    recipient_email = 'casvel320@gmail.com'
    email_password = 'zuben320'

    smtp_server = 'smtp.live.com'
    smtp_port = 587

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = 'Form Data'

    # Attach the file
    with open('form-data.txt', 'r') as file:
        attachment = MIMEText(file.read())
        attachment.add_header('Content-Disposition', 'attachment', filename='form-data.txt')
        message.attach(attachment)

    # Set up the SMTP server
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, email_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

    print('Email sent successfully!')

if __name__ == '__main__':
    app.run(debug=True)

