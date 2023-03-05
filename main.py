from scrape_departments import scrape_kohls
from send_email import send_email


def main():
    kohls_clearance_csv = scrape_kohls()
    send_email(kohls_clearance_csv)


if __name__ == '__main__':
    main()
