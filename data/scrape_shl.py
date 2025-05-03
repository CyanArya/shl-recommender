# scrape_shl.py

import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_shl_catalog():
    base_url = "https://www.shl.com/solutions/products/product-catalog/"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    data = []
    for card in soup.select('.product-card'):
        name = card.select_one('h3').text.strip()
        url = card.select_one('a')['href']
        duration = "N/A"  # If duration is available, scrape it
        remote = "Yes" if "remote" in card.text.lower() else "No"
        adaptive = "Yes" if "adaptive" in card.text.lower() else "No"
        test_type = "N/A"  # If test type is available, scrape it

        data.append({
            "name": name,
            "url": "https://www.shl.com" + url,
            "duration": duration,
            "remote": remote,
            "adaptive": adaptive,
            "test_type": test_type
        })

    if data:
        df = pd.DataFrame(data)
        df.to_csv("shl_assessments.csv", index=False)
        print("✅ Data saved to shl_assessments.csv")
    else:
        print("❌ No data scraped")
        
if __name__ == "__main__":
    scrape_shl_catalog()
