import os
import requests

if not os.path.exists('../svg'):
    os.makedirs('../svg')

stocks = '../img/img.txt'

def download_svg(url):
    response = requests.get(url)
    if response.status_code == 200:
        file_name = os.path.basename(url)
        with open(os.path.join('../svg', file_name), 'wb') as file:
            file.write(response.content)
            return True
    return False

with open(stocks, 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    if url.strip():
        success = download_svg(url)
        if success:
            print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url}")

print("SVG files have been saved")
