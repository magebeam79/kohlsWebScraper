import os


# Define Twilio parameters
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
from_number = os.environ.get('TWILIO_PHONE_NUMBER')
to_number = os.environ.get('PHONE_NUMBER')

# Define email parameters
sender_email = os.environ.get('EMAIL_ADDRESS')
receiver_email = os.environ.get('RECEIVER_ADDRESS')
email_password = os.environ.get('SECRET_KEY')