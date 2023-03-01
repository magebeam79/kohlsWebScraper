import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime


departments = [
    {'name': 'accessories', 'url': 'https://www.kohls.com/catalog/clearance-accessories.jsp?CN=Promotions:Clearance+Department:Accessories&kls_sbp=90595572255358814293312850185484413129&pfm=browse%20refine&PPP=48&S=7&sks=true'},
    {'name': 'beauty', 'url': 'https://www.kohls.com/catalog/clearance-beauty.jsp?CN=Promotions:Clearance+Department:Beauty&kls_sbp=90595572255358814293312850185484413129&pfm=browse%20refine&PPP=48&S=7&sks=true'},
    {'name': 'bed-bath', 'url': 'https://www.kohls.com/catalog/clearance-bed-bath.jsp?CN=Promotions:Clearance+Department:Bed%20%26%20Bath&pfm=browse%20refine&kls_sbp=90595572255358814293312850185484413129&PPP=48&S=7&sks=true'},
    {'name': 'health', 'url': 'https://www.kohls.com/catalog/clearance-health-personal-care.jsp?CN=Promotions:Clearance+Department:Health%20%26%20Personal%20Care&pfm=browse%20refine&kls_sbp=90595572255358814293312850185484413129&PPP=48&S=7&sks=true'},
    {'name': 'home', 'url': 'https://www.kohls.com/catalog/clearance-home-decor.jsp?CN=Promotions:Clearance+Department:Home%20Decor&kls_sbp=90595572255358814293312850185484413129&pfm=browse%20refine&PPP=48&S=7&sks=true'},
    {'name': 'kitchen', 'url': 'https://www.kohls.com/catalog/clearance-kitchen-dining.jsp?CN=Promotions:Clearance+Department:Kitchen%20%26%20Dining&pfm=browse%20refine&kls_sbp=90595572255358814293312850185484413129&PPP=48&S=7&sks=true'},
    {'name': 'sports', 'url': 'https://www.kohls.com/catalog/clearance-sports-fitness.jsp?CN=Promotions:Clearance+Department:Sports%20%26%20Fitness&pfm=browse%20refine&kls_sbp=90595572255358814293312850185484413129&PPP=48&S=7&sks=true'},
    {'name': 'shoes', 'url': 'https://www.kohls.com/catalog/clearance-shoes.jsp?CN=Promotions:Clearance+Department:Shoes&kls_sbp=90595572255358814293312850185484413129&pfm=browse%20refine&PPP=48&S=7&sks=true'},
    {'name': 'toys', 'url': 'https://www.kohls.com/catalog/sale-toys.jsp?CN=Promotions:Clearance+Promotions:Sale+Department:Toys&BL=y&pfm=browse%20refine&kls_sbp=05834574949241830242529155580587980870&PPP=48&S=7&sks=true'},
]

max_pages = 10
data_frames = []
date_string = datetime.datetime.now().strftime('%Y-%m-%d')

for department in departments:
    print(f"Scraping department: {department['name']}")
    department_data = []

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

            if percentage_discount >= 70:
                data_dict = {'Product Name': title, 'Orig Price': original_price, 'Sale Price': sale_price,
                             'Discount': percentage_discount}
                department_data.append(data_dict)

            next_link = soup.find('a', {'class': 'ce-pgntn'})
            if not next_link:
                break
            page += 1
            if page == 2:
                url = url + '&WS=48'
            else:
                url = url + f'&WS={48 * (page - 1)}'

    department_df = pd.DataFrame(department_data)
    pd.set_option('display.max_columns', None)
    department_df.to_csv(f'kohls_{department["name"]}_{date_string}.csv', index=False)

    # Add a delay between each request
    time.sleep(2)

