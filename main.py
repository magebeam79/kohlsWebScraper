import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from department_urls import departments
from credentials import *
from sms import send_sms_alert


subject = 'Kohls Clearance Data'
body = 'Please find attached the Kohls Clearance data.'
email_body = 'Please find attached the Kohls Clearance data.'
email_password = os.environ.get('SECRET_KEY')


def main():
    kohls_clearance_csv = scrape_kohls()
    send_email(kohls_clearance_csv)


def scrape_kohls():
    max_pages = 10
    data_frames = []
    date_string = datetime.datetime.now().strftime('%Y-%m-%d')

    for department in departments:
        print(f"Scraping department: {department['name']}")
        department_products = []

        for page in range(1, max_pages+1):
            if page == 1:
                url = department['url']
            else:
                url = f"{department['url']}&WS={48 * (page-1)}"

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            products = soup.find_all('div', {'class': 'product-description'})

            for product in products:
                # Extract the product title
                title = product.find('div', {'class': 'prod_nameBlock'}).text.strip()

                # Find the div element with a class of 'prod_priceBlock'
                prod_price = product.find('div', {'class': 'prod_priceBlock'})

                # Extract the original product price (lowest)
                try:
                    original_price_range = prod_price.find('div', {'class': 'prod_price_original'}).text.strip().split()
                    original_price = float(original_price_range[1].replace('$', '').replace(',', ''))
                except IndexError:
                    original_price = float(prod_price.find('div', {'class': 'prod_price_original'}).text.strip().split()[0].
                                           replace('$', '').replace(',', ''))

                # Extract the sale price
                sale_price_range = prod_price.find('span', {'class': 'prod_price_amount'}).text.strip().split()
                sale_price = float(sale_price_range[0].replace('$', '').replace(',', '')) if sale_price_range else original_price

                # Calculate percentage discount
                if original_price and sale_price:
                    percentage_discount = round(((original_price - sale_price) / original_price) * 100, 2)
                else:
                    percentage_discount = None

                if percentage_discount >= 90:
                    send_sms_alert(title, department['name'], original_price, sale_price, percentage_discount)

                if percentage_discount >= 70:
                    orig_price_formatted = "${:.2f}".format(original_price)
                    sale_price_formatted = "${:.2f}".format(sale_price)
                    discount_formatted = "{:.0%}".format(percentage_discount/100)
                    data_dict = {'Department': department['name'],
                                 'Product Name': title,
                                 'Orig Price': orig_price_formatted,
                                 'Sale Price': sale_price_formatted,
                                 'Discount': discount_formatted}
                    department_products.append(data_dict)

                next_page = soup.find('a', {'class': 'ce-pgntn'})
                if not next_page:
                    break
                page += 1
                if page == 2:
                    url = url + '&WS=48'
                else:
                    url = url + f'&WS={48 * (page - 1)}'

            time.sleep(1)

        print(f"Finished scanning {department['name']}")

        # departments sale items appended together
        data_frames.append(pd.DataFrame(department_products))

    df = pd.concat(data_frames)
    kohls_clearance_csv = f'kohls_clearance_{date_string}.csv'
    df.to_csv(kohls_clearance_csv, index=False)

    print('Scraping complete!')
    return kohls_clearance_csv


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


if __name__ == '__main__':
    main()
