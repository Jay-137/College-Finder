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

        # Click on the Scholarship tab
        try:
            scholarship_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Scholarship"]')
            scholarship_tab.click()
            time.sleep(2)  # Wait for the scholarship page to load

            # Try to locate scholarship information from the first XPath
            scholarships = driver.find_elements(By.XPATH, '//div[@id="listing-article"]/p')
            if len(scholarships) < 5:
                # If less than 5, check the second XPath
                scholarships += driver.find_elements(By.XPATH, '//div[@class="cdcms_scholarships"]//p')

                # If still less than 5, check the third XPath
                if len(scholarships) < 5:
                    scholarships += driver.find_elements(By.XPATH, '//p[@class="jsx-2056580160 overflow-hidden false article-new ml-1 d-inline"]')

            # Extract up to 5 unique scholarship descriptions
            scholarship_texts = [scholarship.text.strip() for scholarship in scholarships][:5]

            if scholarship_texts:
                # Concatenate to make sure we have a maximum of 5 entries
                for text in scholarship_texts:
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Scholarship Info': text
                    })
                print(f"Scraped {len(scholarship_texts)} scholarship entries for {college_name} ({count})")
            else:
                # If no scholarship information found
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Scholarship Info': "No data found"
                })
                print(f"No scholarship data found for {college_name} ({count})")

        except Exception as e:
            print(f"Scholarship tab not found for {college_name} ({count})")
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Scholarship Info': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count})")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Scholarship Info': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\scholarship_data_1000.csv", index=False)

# Close the browser
driver.quit()
