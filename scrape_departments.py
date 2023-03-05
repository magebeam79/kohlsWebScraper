import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import datetime
from department_urls import departments
from sms import send_sms_alert
import concurrent.futures


def scrape_department(department):
    max_pages = 20
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

            # Extract the original product price
            original_price_range_elem = prod_price.find('div', {'class': 'prod_price_original'})
            if original_price_range_elem is not None:
                original_price_range = original_price_range_elem.text.strip().split()
                if len(original_price_range) > 0:
                    try:
                        if original_price_range[1] == '-':
                            original_price = float(original_price_range[2].replace('$', '').replace(',', ''))
                        else:
                            original_price = float(original_price_range[1].replace('$', '').replace(',', ''))
                    except IndexError:
                        if original_price_range[0] != '-':
                            original_price = float(original_price_range[0].replace('$', '').replace(',', ''))
                        else:
                            original_price = None
                else:
                    original_price = None
            else:
                original_price = None

            # Extract the sale price
            sale_price_range = prod_price.find('span', {'class': 'prod_price_amount'}).text.strip().split()
            sale_price = float(sale_price_range[0].replace('$', '').replace(',', '')) if sale_price_range else original_price

            # Calculate percentage discount
            if original_price and sale_price:
                percentage_discount = round(((original_price - sale_price) / original_price) * 100, 2)
            else:
                percentage_discount = None

            if percentage_discount is not None and  percentage_discount >= 90:
                send_sms_alert(title, department['name'], original_price, sale_price, percentage_discount)

            if percentage_discount is not None and  percentage_discount >= 70:
                orig_price_formatted = "${:.2f}".format(original_price)
                sale_price_formatted = "${:.2f}".format(sale_price)
                discount_formatted = "{:.0%}".format(percentage_discount/100)
                data_dict = {'Department': department['name'],
                             'Product Name': title,
                             'Orig Price': orig_price_formatted,
                             'Sale Price': sale_price_formatted,
                             'Discount': discount_formatted}
                department_data.append(data_dict)

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
    return department_data


def scrape_kohls():
    date_string = datetime.datetime.now().strftime('%Y-%m-%d')
    data_frames = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Scrape each department in parallel
        futures = [executor.submit(scrape_department, department) for department in departments]

        # Collect the results
        for future in concurrent.futures.as_completed(futures):
            department_data = future.result()
            data_frames.append(pd.DataFrame(department_data))

    df = pd.concat(data_frames)
    kohls_csv = f'kohls_clearance_{date_string}.csv'
    df.to_csv(kohls_csv, index=False)

    print('Scraping complete!')
    return kohls_csv


#     print(f"Finished scanning {department['name']}")
#     data_frames.append(pd.DataFrame(department_data))
#
# df = pd.concat(data_frames)
# kohls_csv = f'kohls_clearance_{date_string}.csv'
# df.to_csv(kohls_csv, index=False)
#
# print('Scraping complete!')
# return kohls_csv