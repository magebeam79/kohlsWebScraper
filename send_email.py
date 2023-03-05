import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from credentials import *


subject = 'Kohls Clearance Data'
email_body = 'Please find attached the Kohls Clearance data.'


def send_email(kohls_clearance_csv):

    # Create message and set headers
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    # Add body to email
    message.attach(MIMEText(email_body, "plain"))

    # Open the CSV file in bytestream mode and attach it to the email
    with open(kohls_clearance_csv, 'rb') as f:
        attach = MIMEApplication(f.read(), _subtype="csv")
        attach.add_header('Content-Disposition', 'attachment', filename=kohls_clearance_csv)
        message.attach(attach)

    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)
    session.starttls()
    session.login(sender_email, email_password)

    # Convert the message to a string and send the mail
    text = message.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()

    print('Email sent successfully!')