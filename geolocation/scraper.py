import requests
from lxml import html
import pandas as pd

BASE_URL = "https://geokeo.com/database/city/in/{}/"

TABLE_XPATH = '/html/body/main/div/table[1]/tbody/tr'

data = []

TOTAL_PAGES = 27

def scrape_page(page_number):
    url = BASE_URL.format(page_number)
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch page {page_number}")
        return
    
    tree = html.fromstring(response.content)
    rows = tree.xpath(TABLE_XPATH)
    
    for row in rows:
        city_id = row.xpath('td[1]/text()')[0]
        city_name = row.xpath('td[2]/text()')[0]
        latitude = row.xpath('td[4]/text()')[0]
        longitude = row.xpath('td[5]/text()')[0]
        
        data.append({
            "ID": city_id,
            "City": city_name,
            "Latitude": latitude,
            "Longitude": longitude
        })

def main():
    for page in range(1, TOTAL_PAGES + 1):
        scrape_page(page)
    
    df = pd.DataFrame(data)
    df.to_csv('city_data.csv', index=False)

if __name__ == "__main__":
    main()
