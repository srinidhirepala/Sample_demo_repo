from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Step 1: Browser setup cheyali
options = Options()
# options.add_argument("--headless")  # Headless mode off rakunda browser chudali
driver = webdriver.Chrome(options=options)

# Step 2: Website ki vellali
url = "https://housing.com/in/buy/plots-land"  # Lands section URL (check Housing.com)
driver.get(url)
time.sleep(3)  # Page load avvali

# Step 3: User-defined location istham
location = input("Enter location (ex: Hyderabad): ")  # User nunchi location teeskuntam
search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search for locality, property or landmark']")  # Search bar XPath
search_box.send_keys(location)
search_box.send_keys(Keys.ENTER)
time.sleep(5)  # Search results load avvali

# Step 4: Data store cheyadaniki list
land_data = []

# Step 5: Pages navigation and extraction
while True:
    # Listings anni teeskuntam (HTML class based on Housing.com)
    listings = driver.find_elements(By.CLASS_NAME, "css-1nr7r9e")  # Example class, inspect chesi change cheyali
    
    for listing in listings:
        try:
            # Land details extract cheyali
            sqft = "NA"
            facing = "NA"
            price = "NA"
            location_text = "NA"
            
            # Try to get each attribute, missing aithe NA
            try:
                sqft = listing.find_element(By.XPATH, ".//div[contains(text(), 'sqft')]").text
            except:
                pass
            
            try:
                facing = listing.find_element(By.XPATH, ".//span[contains(text(), 'Facing')]").text
            except:
                pass
            
            try:
                price = listing.find_element(By.CLASS_NAME, "price").text  # Price class
            except:
                pass
            
            try:
                location_text = listing.find_element(By.CLASS_NAME, "locality").text  # Location class
            except:
                pass

            # Dictionary lo store cheyali
            land_details = {
                "Location": location_text,
                "Square Feet": sqft,
                "Facing": facing,
                "Price": price
            }
            land_data.append(land_details)
            print(land_details)  # Check cheyadaniki print

        except Exception as e:
            print(f"Error in listing: {e}")
            continue
    
    # Next page ki vellali
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 'next')]")  # Next button XPath
        next_button.click()
        time.sleep(3)  # Page load avvali
    except:
        print("No more pages, extraction done!")
        break

# Step 6: CSV file lo save cheyali
df = pd.DataFrame(land_data)
df.to_csv("land_data.csv", index=False)
print("Data saved to land_data.csv")

# Browser close cheyali
driver.quit()