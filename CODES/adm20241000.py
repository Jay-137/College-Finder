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

        # Click on the specified button using the updated XPath
        try:
            courses_button = driver.find_element(By.XPATH, '//a[@data-ga-title="Admission 2024" or @data-ga-title="Admission"]')
            courses_button.click()
            time.sleep(2)  # Wait for the new page to load

            # Initialize variable to store admission highlight text
            

            info = ""  # Initialize info as an empty string

            # Function to get text if it's not "Table of Contents"
            def get_text_if_not_toc(element):
                text = element.text.strip()
                return text if text.lower() != "table of content" else ""

            # Attempt to scrape from the first XPath
            try:
                admission_highlights_1 = driver.find_element(By.XPATH, '//*[@id="listing-article"]/div[1]/div/p[1]')
                text_1 = get_text_if_not_toc(admission_highlights_1)
                if text_1:
                    info += text_1
            except Exception as e:
                print(f"First admission highlights path not found for {college_name}")

            # Attempt to scrape from the second XPath
            try:
                admission_highlights_2 = driver.find_element(By.XPATH, '//*[@id="listing-article"]/div[1]/p[1]')
                text_2 = get_text_if_not_toc(admission_highlights_2)
                if text_2:
                    info += " | " + text_2 if info else text_2
            except Exception as e:
                print(f"Second admission highlights path not found for {college_name}")

            # Attempt to scrape from the third XPath
            try:
                admission_highlights_3 = driver.find_element(By.XPATH, '//*[@id="listing-article"]/div[1]/div/p[2]')
                text_3 = get_text_if_not_toc(admission_highlights_3)
                if text_3:
                    info += " | " + text_3 if info else text_3
            except Exception as e:
                print(f"Third admission highlights path not found for {college_name}")

            # Check if no data was found in any of the paths
            if not info:
                info = "no data found"





        except Exception as e:
            info = "no data found"
            print(f"Button not found for {college_name}: {e}")

        # Append the result to all_data list
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Info': info
        })

        # Debug message indicating that data for the college has been scraped
        print(f"Scraped data for {college_name} ({counter})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url}: {e}")
    counter += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file named adm2024_500.csv
scraped_df.to_csv("DATA\\adm2024_1000.csv", index=False)

# Close the browser
driver.quit()
