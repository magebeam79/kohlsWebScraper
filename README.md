# Kohls Webscraper

This is a Python program that scrapes Kohls.com for toy items on sale and clearance, and saves the data to a CSV file.

## Getting Started

### Prerequisites

To run this program, you need Python 3.x installed on your system. You also need to have the following Python libraries installed:
* requests
* beautifulsoup4
* pandas

You can install them using pip by running:

pip install -r requirements.txt

### Installing

1. Clone this repository to your local machine.
2. In the terminal, navigate to the directory where you cloned this repository.
3. Run `python kohlsWebscraper.py`.

## Usage

The program scrapes Kohls.com for toy items on sale and clearance, and saves the data to a CSV file named `kohlsToys_<date>.csv`, where `<date>` is the current date in `YYYY-MM-DD` format. The CSV file contains the following columns:
* Product Name: The name of the toy product.
* Orig Price: The original price of the toy product.
* Sale Price: The sale price of the toy product.
* Discount: The percentage discount of the toy product.
