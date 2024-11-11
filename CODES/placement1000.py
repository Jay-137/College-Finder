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

        # Try to click the Placement button
        try:
            placement_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Placement"]')
            placement_tab.click()
            time.sleep(3)  # Wait for the page to load after clicking
        except:
            # Click the arrow button to reveal more options if the Placement button is not visible
            try:
                arrow_button = driver.find_element(By.XPATH, '//div[@class="jsx-3207461571 right-arrow d-flex flex-column justify-content-center pointer arrow position-absolute d-block bg-white rounded"]')
                arrow_button.click()
                time.sleep(1)
                placement_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Placement"]')
                placement_tab.click()
                time.sleep(2)
            except:
                print(f"Placement tab not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Company': "No data found",
                    'Package': "No data found",
                    'Job Roles': "No data found",
                    'Headings': "No data found"
                })
                count += 1
                continue

        # Find the first table and extract the data
        try:
            table = driver.find_element(By.XPATH, '//div[@class="table-responsive"]')
            rows = table.find_elements(By.XPATH, './/tr')

            # Extract column headers
            headers = [header.text.strip() for header in rows[0].find_elements(By.XPATH, './/th')]
            if not headers:
                headers=[header.text.strip() for header in rows[0].find_elements(By.XPATH, './/td')]
            headings_text = ", ".join(headers) if headers else "No headings found"

            # Extract table data based on the number of columns
            for row in rows[1:]:  # Skip the header row
                columns = row.find_elements(By.XPATH, './/td')
                if len(columns) == 2:  # Handle case with 2 columns
                    company = columns[0].text.strip() if columns[0].text else "No data"
                    package = columns[1].text.strip() if columns[1].text else "No data"
                    job_roles = "No data found"

                    # Append the data to the list
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Company': company,
                        'Package': package,
                        'Job Roles': job_roles,
                        'Headings': headings_text
                    })

                elif len(columns) >= 3:  # Handle case with 3 columns
                    company = columns[0].text.strip() if columns[0].text else "No data"
                    package = columns[1].text.strip() if columns[1].text else "No data"
                    job_roles = columns[2].text.strip() if columns[2].text else "No data"

                    # Append the data to the list
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Company': company,
                        'Package': package,
                        'Job Roles': job_roles,
                        'Headings': headings_text
                    })

            print(f"Scraped placement data for {college_name} ({count})")
        except:
            # No placement data found
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Company': "No data found",
                'Package': "No data found",
                'Job Roles': "No data found",
                'Headings': "No data found"
            })
            print(f"No placement data found for {college_name} ({count})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count}): {e}")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Company': "No data found",
            'Package': "No data found",
            'Job Roles': "No data found",
            'Headings': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\placement_data_1000.csv", index=False)

# Close the browser
driver.quit()
