import csv
import os
from playwright.sync_api import sync_playwright

IMG_URL = "https://s3-symbol-logo.tradingview.com/"


def find_first_image_with_src_prefix(page):
    all_images = page.query_selector_all('img')
    for img in all_images:
        src_attribute = img.get_attribute('src')
        if src_attribute and src_attribute.startswith(IMG_URL):
            return img
    return None


print("Starting crawling")
with sync_playwright() as p:
    page = p.chromium.launch().new_page()

    if not os.path.exists('../img'):
        os.makedirs('../img')
    with open('../data/stocks.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)

        with open('../img/img.txt', 'w') as txtfile:
            for row in csv_reader:
                print(f"Evaluating ticker: {row[0]}")
                if len(row) > 0:
                    url = f"https://www.tradingview.com/symbols/{row[1]}-{row[0]}/"

                    page.goto(url)
                    img_element = find_first_image_with_src_prefix(page)

                    if img_element:
                        src_attribute = img_element.get_attribute('src')
                        txtfile.write(f"{src_attribute}\n")
                        print(f"SUCCESS: Found an url for ticker: {row[0]}")
                    else:
                        fallbackUrl = f"https://www.tradingview.com/symbols/{row[2]}-{row[0]}/"
                        page.goto(fallbackUrl)
                        img_element_retry = find_first_image_with_src_prefix(page)
                        if img_element_retry:
                            src_attribute = img_element_retry.get_attribute('src')
                            txtfile.write(f"{src_attribute}\n")
                            print(f"SUCCESS: Found an url for ticker: {row[0]}")
                        else:
                            txtfile.write(f"Not found for {url} or {fallbackUrl}\n")
                            print(f"ERROR: failed to find an url for ticker: {row[0]}")

    page.close()

print("Results have been written to 'img/img.txt'.")
