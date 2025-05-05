from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
import time

def check_for_new_filings():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use WebDriver Manager to auto-fetch compatible ChromeDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://efdsearch.senate.gov/search/")
    time.sleep(2)

    search_button = driver.find_element(By.ID, "searchbtn")
    search_button.click()
    time.sleep(5)

    rows = driver.find_elements(By.CSS_SELECTOR, "table#filedReports tbody tr")
    new_data = []
    existing = set()

    if os.path.exists("data/log.csv"):
        existing_df = pd.read_csv("data/log.csv")
        existing = set(existing_df["Document URL"].values)

    for row in rows:
        cols = row.find_elements(By.TAG_NAME, "td")
        if len(cols) < 4:
            continue
        name = cols[0].text.strip()
        office = cols[1].text.strip()
        date = cols[2].text.strip()
        url = cols[3].find_element(By.TAG_NAME, "a").get_attribute("href")

        if url not in existing:
            new_data.append({
                "Name": name,
                "Office": office,
                "Filing Date": date,
                "Document URL": url
            })

    driver.quit()

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