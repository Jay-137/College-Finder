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

        # Try to click the Hostel button
        try:
            hostel_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Hostel"]')
            hostel_tab.click()
            time.sleep(2)  # Wait for the page to load after clicking
        except:
            # Click the arrow button to reveal more options if the Hostel button is not visible
            try:
                arrow_button = driver.find_element(By.XPATH, '//div[@class="jsx-3207461571 right-arrow d-flex flex-column justify-content-center pointer arrow position-absolute d-block bg-white rounded"]')
                arrow_button.click()
                time.sleep(1)
                hostel_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Hostel"]')
                hostel_tab.click()
                time.sleep(2)
            except:
                print(f"Hostel tab not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Info': "No data found"
                })
                count += 1
                continue

        # Extract hostel data
        hostel_data = driver.find_elements(By.XPATH, '//div[@class="jsx-2056580160 "]')

        if hostel_data:
            # Limit to a maximum of 5 hostels and add each as a separate row
            for info in hostel_data[:5]:
                data_text = info.text.replace("Hostel Facilities:","").strip()
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Info': data_text
                })

            print(f"Scraped hostel data for {college_name} ({count})")
        else:
            # No hostel data found
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Info': "No data found"
            })
            print(f"No hostel data found for {college_name} ({count})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count}): {e}")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Info': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\hostel_data_1000.csv", index=False)

# Close the browser
driver.quit()
