import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime


max_pages = 10
page = 1
data = []

now = datetime.datetime.now()
date_string = now.strftime('%Y-%m-%d')

for page in range(1, max_pages+1):
    if page == 1:
        url = 'https://www.kohls.com/catalog/sale-toys.jsp?CN=Promotions:Clearance+Promotions:Sale+Department:Toys&BL=y&S=7&PPP=48&pfm=browse%20refine&kls_sbp=05834574949241830242529155580587980870'
        # url = 'https://www.kohls.com/catalog/sale.jsp?CN=Promotions:Clearance+Promotions:Sale&BL=y&kls_sbp=05834574949241830242529155580587980870&pfm=browse&sks=true&PPP=48&S=7'
    else:
        url = f'https://www.kohls.com/catalog/sale-toys.jsp?CN=Promotions:Clearance+Promotions:Sale+Department:Toys&BL=y&pfm=browse%20refine&kls_sbp=05834574949241830242529155580587980870&PPP=48&WS={48 * (page)}&S=7&sks=true'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', {'class': 'product-description'})

    for product in products:
        # Extract the product title
        title = product.find('div', {'class': 'prod_nameBlock'}).text.strip()

        # Find the div element with a class of 'prod_priceBlock'
        prod_price = product.find('div', {'class': 'prod_priceBlock'})

        # Extract the original product price (lowest)
        original_price_range = prod_price.find('div', {'class': 'prod_price_original'}).text.strip().split()[1]
        original_price = float(original_price_range.replace('$', '').replace(',', '')) if original_price_range else None

        # Extract the sale price
        sale_price_range = prod_price.find('span', {'class': 'prod_price_amount'}).text.strip()
        sale_price = float(sale_price_range.split()[0].replace('$', '').replace(',', '')) if sale_price_range else original_price

        # Calculate percentage discount
        if original_price and sale_price:
            percentage_discount = round(((original_price - sale_price) / original_price) * 100, 2)
        else:
            percentage_discount = None

        if percentage_discount >= 50:
            data_dict = {'Product Name': title, 'Orig Price': original_price, 'Sale Price': sale_price,
                         'Discount': percentage_discount}
            data.append(data_dict)

        next_link = soup.find('a', {'class': 'ce-pgntn'})
        if not next_link:
            break
        page += 1
        if page == 2:
            url = url + '&WS=48'
        else:
            url = url + f'&WS={48 * (page - 1)}'

df = pd.DataFrame(data)
pd.set_option('display.max_columns', None)
df.to_csv(f'kohlsToys_{date_string}.csv', index=False)
# print(df)

# Add a delay between each request
time.sleep(2)
