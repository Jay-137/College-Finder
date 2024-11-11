from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Load the CSV file containing college names and URLs
colleges_df = pd.read_csv("DATA\\next_500_colleges.csv")
path = "DATA\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
# Set up Selenium WebDriver
chrome_service = Service(path)  # Replace with your chromedriver path
driver = webdriver.Chrome(service=chrome_service)

# Initialize an empty list to store scraped data
all_data = []
counter = 1

for _, row in colleges_df.iterrows():
    serial_number = row['Serial No.']
    college_name = row['College Name']
    college_url = row['URL']

    # Initialize default row data for this college
    row_data = {
        'Serial No.': serial_number,
        'College Name': college_name,
        'Course': "no data found",
        'Fees': "no data found",
        'Eligibility': "no data found",
        'Application Date': "no data found"
    }

    try:
        # Go to the college URL
        driver.get(college_url)
        time.sleep(2)  # Wait for the page to load

        # Attempt to locate and click the "Courses & Fees" button
        try:
            courses_button = driver.find_element(By.XPATH, '//a[@data-ga-title="Courses & Fees"]')
            courses_button.click()
            time.sleep(1)  # Wait for the new page to load

            # Attempt to locate the table on the new page
            try:
                table = driver.find_element(By.XPATH, '//table[@class="jsx-423712996 table-new table-striped text-title rounded-xl mb-0"]')
                
                # Retrieve table headers and rows
                headers = table.find_elements(By.TAG_NAME, 'th')
                rows = table.find_elements(By.TAG_NAME, 'tr')

                # Get index of required columns
                header_texts = [header.text for header in headers]
                required_columns = ['Course', 'Fees', 'Eligibility', 'Application Date']
                indexes = {col: header_texts.index(col) for col in required_columns if col in header_texts}

                # Extract data for each row (excluding the header row)
                for row in rows[1:]:
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    if columns:
                        # Initialize row data with default values
                        current_row_data = row_data.copy()
                        # Fetch only required columns and update current_row_data
                        for col, idx in indexes.items():
                            value = columns[idx].text
                            if col == 'Fees':
                                # Remove the currency symbol and format as needed
                                value = value.replace('â‚¹', '').replace('₹', '').strip()
                            current_row_data[col] = value

                        # Append the row data to all_data list
                        all_data.append(current_row_data)

                # Debug message indicating data was successfully scraped
                print(f"Scraped data for {college_name} ({counter})")

            except Exception as e:
                # Append default "no data found" row_data if table is not found
                print(f"Table not found for {college_name} ({counter}) at {college_url}: {e}")
                all_data.append(row_data)

        except Exception as e:
            # Append default "no data found" row_data if "Courses & Fees" button is not found
            print(f"'Courses & Fees' button not found for {college_name} ({counter}) at {college_url}: {e}")
            all_data.append(row_data)

    except Exception as e:
        print(f"Error processing {college_name} at {college_url}: {e}")

    counter += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\coursefees1000.csv", index=False)

# Close the browser
driver.quit()
