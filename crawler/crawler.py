import csv
import os
from playwright.sync_api import sync_playwright


def find_first_image_with_src_prefix(page, prefix):
    def find_img_with_src_prefix(page, prefix):
        all_images = page.query_selector_all('img')
        for img in all_images:
            src_attribute = img.get_attribute('src')
            if src_attribute and src_attribute.startswith(prefix):
                return img
        return None

    img_element = find_img_with_src_prefix(page, prefix)
    return img_element

print("Starting crawling")
with sync_playwright() as p:
    browser = p.chromium.launch()

    if not os.path.exists('../img'):
        os.makedirs('../img')
    with open('../data/stocks.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)

        with open('../img/img.txt', 'w') as txtfile:
            for row in csv_reader:
                if len(row) > 0:
                    url = f"https://www.tradingview.com/symbols/{row[1]}-{row[0]}/"
                    prefix_to_match = "https://s3-symbol-logo.tradingview.com/"

                    page = browser.new_page()
                    page.goto(url)

                    img_element = find_first_image_with_src_prefix(page, prefix_to_match)

                    if img_element:
                        src_attribute = img_element.get_attribute('src')
                        txtfile.write(f"{src_attribute}\n")
                    else:
                        fallbackUrl = f"https://www.tradingview.com/symbols/{row[2]}-{row[0]}/"
                        page.goto(fallbackUrl)
                        img_element_retry = find_first_image_with_src_prefix(page, prefix_to_match)
                        if img_element_retry:
                            src_attribute = img_element_retry.get_attribute('src')
                            txtfile.write(f"{src_attribute}\n")
                        else:
                            txtfile.write(f"Not found for {url} or {fallbackUrl}\n")

                    page.close()

    browser.close()

print("Results have been written to 'img/img.txt'.")
