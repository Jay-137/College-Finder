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

        # Try to click the Faculty button
        try:
            faculty_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Faculty"]')
            faculty_tab.click()
            time.sleep(2)  # Wait for the faculty page to load
        except:
            # Click the arrow button to reveal more options if the Faculty button is not visible
            try:
                arrow_button = driver.find_element(By.XPATH, '//div[@class="jsx-3207461571 right-arrow d-flex flex-column justify-content-center pointer arrow position-absolute d-block bg-white rounded"]')
                arrow_button.click()
                time.sleep(1)
                faculty_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Faculty"]')
                faculty_tab.click()
                time.sleep(2)
            except:
                print(f"Faculty tab not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Faculty Name': "No data found",
                    'Title': "No data found",
                    'Department': "No data found",
                    'Phone No': "No data found",
                    'Email': "No data found"
                })
                count += 1
                continue

        # Extract faculty data
        faculty_cards = driver.find_elements(By.XPATH, '//div[@class="jsx-1764708417 jsx-2015978497 faculty-card border border-gray-5 rounded-8 text-center d-flex flex-column align-items-center"]')

        if faculty_cards:
            for card in faculty_cards:
                try:
                    # Extract faculty name
                    try:
                        faculty_name = card.find_element(By.XPATH, './/div[@class="jsx-1764708417 jsx-2015978497 fs-16 font-weight-semi text-primary-black mt-1 text-capitalize"]').text.strip()
                    except:
                        faculty_name = "No data found"

                    # Extract title
                    try:
                        title = card.find_element(By.XPATH, './/div[@class="jsx-1764708417 jsx-2015978497 bg-gray-5 text-capitalize faculty-des fs-12 font-weight-medium text-gray-3 rounded-4 px-3 mt-3"]').text.strip()
                    except:
                        title = "No data found"

                    # Extract department
                    try:
                        department = card.find_element(By.XPATH, './/div[@class="jsx-1764708417 jsx-2015978497 fs-12 font-weight-medium text-dark-grey mt-1 text-capitalize"]').text.strip()
                    except:
                        department = "No data found"

                    # Extract phone number and email
                    try:
                        contact_info_elements = card.find_elements(By.XPATH, './/div[@class="jsx-1764708417 jsx-2015978497 fs-14 font-weight-normal text-dark-grey mt-2 d-flex align-items-center"]')
                        phone_no = contact_info_elements[0].text.strip() if contact_info_elements else "No data found"
                        email = contact_info_elements[1].text.strip() if len(contact_info_elements) > 1 else "No data found"

                        # Check if phone_no contains an email
                        if "@" in phone_no:
                            email = phone_no
                            phone_no = "N/A"
                    except:
                        phone_no = "No data found"
                        email = "No data found"

                    # Append the data to the list
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Faculty Name': faculty_name,
                        'Title': title,
                        'Department': department,
                        'Phone No': phone_no,
                        'Email': email
                    })

                except Exception as e:
                    print(f"Error processing a faculty card for {college_name} ({count}): {e}")
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Faculty Name': "No data found",
                        'Title': "No data found",
                        'Department': "No data found",
                        'Phone No': "No data found",
                        'Email': "No data found"
                    })

            print(f"Scraped faculty data for {college_name} ({count})")
        else:
            # No faculty data found
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Faculty Name': "No data found",
                'Title': "No data found",
                'Department': "No data found",
                'Phone No': "No data found",
                'Email': "No data found"
            })
            print(f"No faculty data found for {college_name} ({count})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count}): {e}")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Faculty Name': "No data found",
            'Title': "No data found",
            'Department': "No data found",
            'Phone No': "No data found",
            'Email': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\faculty_data_1000.csv", index=False)

# Close the browser
driver.quit()
