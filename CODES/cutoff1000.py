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

        # Click on the CutOff tab
        try:
            cutoff_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="CutOff"]')
            cutoff_tab.click()
            time.sleep(2)  # Wait for the cutoff page to load

            # Try to find the table for cutoff marks
            try:
                cutoff_rows = driver.find_elements(By.XPATH, '//tbody[@class="jsx-347914569"]/tr')
                if cutoff_rows:
                    for row in cutoff_rows:
                        # Extract course name and cutoff mark for each row
                        course_name = row.find_element(By.XPATH, './td[1]').text.strip()
                        cutoff_mark = row.find_element(By.XPATH, './td[2]').text.strip()

                        # Append each course-cutoff pair as a separate entry
                        all_data.append({
                            'Serial No.': serial_number,
                            'College Name': college_name,
                            'Course Name': course_name,
                            'Cutoff Mark': cutoff_mark
                        })
                else:
                    # If rows are not found, mark as "No data found"
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Course Name': "No data found",
                        'Cutoff Mark': "No data found"
                    })

                print(f"Scraped cutoffs for {college_name} ({count})")

            except Exception as e:
                print(f"Cutoff table or rows not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Course Name': "No data found",
                    'Cutoff Mark': "No data found"
                })

        except Exception as e:
            print(f"Cutoff tab not found for {college_name} ({count})")
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Course Name': "No data found",
                'Cutoff Mark': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count})")

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\cutoff_marks_1000.csv", index=False)

# Close the browser
driver.quit()
