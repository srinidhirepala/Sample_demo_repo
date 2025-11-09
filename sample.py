from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Run in headless mode (no GUI)
driver = webdriver.Chrome(options=options)

# URL for Craigslist land listings in New York
url = "https://newyork.craigslist.org/search/rea?query=land"
driver.get(url)

time.sleep(2)  # Allow time for the page to load

# Lists to store data
titles = []
prices = []
locations = []
links = []

# Scrape listings
listings = driver.find_elements(By.CSS_SELECTOR, ".result-info")

for listing in listings:
    try:
        # Extract title
        title = listing.find_element(By.CSS_SELECTOR, ".result-title").text
        titles.append(title)

        # Extract price
        price_element = listing.find_elements(By.CSS_SELECTOR, ".result-price")
        price = price_element[0].text if price_element else "N/A"
        prices.append(price)

        # Extract location
        location_element = listing.find_elements(By.CSS_SELECTOR, ".result-hood")
        location = location_element[0].text.strip(" ()") if location_element else "N/A"
        locations.append(location)

        # Extract URL
        link = listing.find_element(By.CSS_SELECTOR, ".result-title").get_attribute("href")
        links.append(link)

    except Exception as e:
        print(f"Error processing listing: {e}")

driver.quit()

# Create DataFrame
data = {
    "Title": titles,
    "Price": prices,
    "Location": locations,
    "URL": links
}
df = pd.DataFrame(data)

# Save to CSV
df.to_csv("craigslist_land_listings.csv", index=False)

print("Data has been successfully scraped and saved to 'craigslist_land_listings.csv'.")