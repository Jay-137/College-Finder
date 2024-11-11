from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Load the CSV file containing college names and URLs
colleges_df = pd.read_csv("DATA\\next_500_colleges.csv")
path = "DATA\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
# Set up Selenium WebDriver (example for Chrome)
chrome_service = Service(path)  # Replace with your chromedriver path
driver = webdriver.Chrome(service=chrome_service)

# Initialize an empty list to store scraped data
all_data = []
counter = 1

# Loop through each college in the DataFrame
for _, row in colleges_df.iterrows():
    serial_number = row['Serial No.']
    college_name = row['College Name']
    college_url = row['URL']

    try:
        # Go to the college URL
        driver.get(college_url)
        time.sleep(1)  # Wait for the page to load

        # Click on the Distance Education button using the provided XPath
        try:
            distance_education_button = driver.find_element(By.XPATH, '//a[@data-ga-title="Distance Education"]')
            distance_education_button.click()
            time.sleep(2)  # Wait for the new page to load

            # Attempt to scrape all paragraphs under the specified XPath
            try:
                paragraphs = driver.find_elements(By.XPATH, '//*[@id="listing-article"]/div/p')
                distance_education_info = " | ".join([para.text.strip() for para in paragraphs if para.text.strip()])
                if not distance_education_info:
                    distance_education_info = "no data found"
            except Exception as e:
                distance_education_info = "no data found"
                print(f"NO DATA FOUND in Distance Education section for {college_name}")

        except Exception as e:
            distance_education_info = "no data found"
            print(f"Distance Education BUTTON not found for {college_name}")

        # Append the result to all_data list
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Distance Education Info': distance_education_info
        })

        # Debug message indicating that data for the college has been scraped
        print(f"Scraped Distance Education data for {college_name} ({counter})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url}: {e}")
    counter += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file named distance_education_500.csv
scraped_df.to_csv("DATA\\distance_education_1000.csv", index=False)

# Close the browser
driver.quit()
