import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

SEARCH_URL = "https://efdsearch.senate.gov/search/"

def check_for_new_filings():
    session = requests.Session()
    
    # This mimics a form submission on the site
    response = session.post(SEARCH_URL, data={})
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "filedReports"})
    
    if not table:
        print("No table found on page.")
        return []

    rows = table.find("tbody").find_all("tr")
    new_data = []
    existing = set()

    # Load previously logged URLs
    if os.path.exists("data/log.csv"):
        existing_df = pd.read_csv("data/log.csv")
        existing = set(existing_df["Document URL"].values)

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        name = cols[0].get_text(strip=True)
        office = cols[1].get_text(strip=True)
        date = cols[2].get_text(strip=True)
        link = cols[3].find("a")
        url = link["href"] if link else ""

        if url and url not in existing:
            new_data.append({
                "Name": name,
                "Office": office,
                "Filing Date": date,
                "Document URL": url
            })

    if new_data:
        df_new = pd.DataFrame(new_data)
        if os.path.exists("data/log.csv"):
            df_existing = pd.read_csv("data/log.csv")
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        else:
            df_combined = df_new

        os.makedirs("data", exist_ok=True)
        df_combined.to_csv("data/log.csv", index=False)

    return new_data