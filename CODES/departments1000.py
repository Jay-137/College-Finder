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
count=1
# Loop through each college in the DataFrame
for _, row in colleges_df.iterrows():
    serial_number = row['Serial No.']
    college_name = row['College Name']
    college_url = row['URL']

    try:
        # Go to the college URL
        driver.get(college_url)
        time.sleep(1)  # Wait for the page to load

        # Click on the Department tab
        try:
            department_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Department"]')
            department_tab.click()
            time.sleep(2)  # Wait for the department page to load

            # Try to find department and location elements
            department_elements = driver.find_elements(By.XPATH, '//a[@class="jsx-3613386350 fs-16 font-weight-semi text-primary-black mb-1"]')
            location_elements = driver.find_elements(By.XPATH, '//*[@id="__next"]/div[2]/section/div[1]/div[3]/div/div/section/div/div[1]/div/div[1]/div[1]/span')

            # Check if both departments and locations were found
            if department_elements and location_elements:
                for dept_element, loc_element in zip(department_elements, location_elements):
                    department = dept_element.text.strip()
                    location = loc_element.text.strip()
                    
                    # Append each department-location pair as a separate entry
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Department': department,
                        'Location': location
                    })
            else:
                # If elements are not found, mark as "No data found"
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Department': "No data found",
                    'Location': "No data found"
                })

            print(f"Scraped departments for {college_name}({count})")

        except Exception as e:
            print(f"Department tab not found for {college_name}({count})")
            # Append "No data found" if the Department tab is not accessible
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Department': "No data found",
                'Location': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url}({count})")
    count+=1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\departments_1000.csv", index=False)

# Close the browser
driver.quit()
