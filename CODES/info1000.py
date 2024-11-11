from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Load the CSV file containing college names and URLs
colleges_df = pd.read_csv("DATA\\next_500_colleges.csv")
path = "DATA\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
# Set up Selenium WebDriver (example for Chrome)
chrome_service = Service(path)
driver = webdriver.Chrome(service=chrome_service)

# Initialize an empty list to store scraped data
all_data = []
count = 1

# Loop through each college in the DataFrame
for _, row in colleges_df.iterrows():
    serial_number = row['Serial No.']
    college_name = row['College Name']
    college_url = row['URL']

    try:
        # Go to the college URL
        driver.get(college_url)
        time.sleep(1)  # Wait for the page to load

        # Attempt to scrape info data
        try:
            # Find the first instance of the info paragraph
            try:
                info_element = driver.find_element(By.XPATH, '//div[@class="cdcms_college_highlights"]//p')
            except:
                try:
                    info_element= driver.find_element(By.XPATH,'//div[@class="college_highlights"]//p')
                except:
                    try:
                        info_element= driver.find_element(By.XPATH,'//div[@class="cdcms_section1"]//p')
                    except:
                        try:
                            info_element= driver.find_element(By.XPATH,'//div[@class="cdcms_admission_highlights"]//p')
                        except:
                            info_element= driver.find_element(By.XPATH,'//div[@id="listing-article"]//p')
                        
                    
            info_data = info_element.text.strip() if info_element else "No data found"

            # Append the data for the current college
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Info Data': info_data
            })

            print(f"Scraped info data for {college_name} ({count})")

        except Exception as e:
            print(f"Info data not found for {college_name} ({count})")
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Info Data': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count})")

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\info_data_1000.csv", index=False)

# Close the browser
driver.quit()
