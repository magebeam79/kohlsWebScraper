# Kohls Webscraper

This is a Python program that scrapes Kohls.com for clearance items, collects the data in a CSV file, and sends it to an email address. It also sends a text message to a phone number using the Twilio API whenever an item is found at a 90% discount or more.

## Getting Started

### Prerequisites

To run this program, you need Python 3.x installed on your system. You also need to have the following Python libraries installed:
* requests
* beautifulsoup4
* pandas
* twilio
* SMTP


You can install them using pip by running:

pip install -r requirements.txt

### Installing

1. Clone this repository to your local machine.
2. In the terminal, navigate to the directory where you cloned this repository.
3. Run `python kohlsWebscraper.py`.

### Setting up the Twilio Account
To use the Twilio API, you must create an account on Twilio. Once you have created an account, create a new project, and obtain the Account SID and Auth Token from the dashboard. You will also need to purchase a phone number to send the text messages. These details can be added to the environment variables of the system.

## Usage

The program scrapes specific Kohls URLs for clearance items, and saves the data to a CSV file named `kohls_clearance_<date>.csv`, where `<date>` is the current date in `YYYY-MM-DD` format. The CSV file contains the following columns:
* Department Name: The name of the product department.
* Product Name: The name of the sale product.
* Orig Price: The original price of the product.
* Sale Price: The sale price of the product.
* Discount: The percentage discount of the product.
