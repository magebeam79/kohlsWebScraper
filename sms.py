from twilio.rest import Client
from credentials import *


def send_sms_alert(title, department_name, original_price, sale_price, percentage_discount):
    # Create a Twilio client object
    client = Client(account_sid, auth_token)

    # Construct the message to send
    message = f"New deal alert: {title} in {department_name} is now {percentage_discount}% off! " \
              f"Original price: {original_price}, sale price: {sale_price}."

    # Send the message
    message = client.messages.create(
        body=message,
        from_=from_number,
        to=to_number
    )

    print(f"SMS sent: {message.sid}")