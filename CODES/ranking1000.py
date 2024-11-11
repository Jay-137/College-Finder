from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time
import re

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

        # Click on the Ranking tab
        try:
            ranking_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Ranking"]')
            ranking_tab.click()
            time.sleep(2)  # Wait for the ranking page to load

            # Check if the "Read More" button is present
            try:
                read_more_button = driver.find_element(By.XPATH, '//div[@data-ga-title="SHOW LESS"]')
                read_more_button.click()
                time.sleep(2)  # Wait for the table to load fully

                # Try to locate the ranking table using the first standard XPath
                try:
                    table = driver.find_element(By.XPATH, '//table[@class="table"]')
                except:
                    table = driver.find_element(By.XPATH, '//table[@class="table table-striped style_table"]')

                # Extract data from the standard table
                if table:
                    rows = table.find_elements(By.XPATH, './/tbody/tr')
                    for row in rows:
                        cells = row.find_elements(By.XPATH, './td')
                        if len(cells) >= 2:
                            ranking_agency = cells[0].text.replace('\n', '|').strip()
                            year = cells[1].text.replace('\n', '|').strip() if len(cells) > 2 else "No data found"
                            rank = cells[-1].text.replace('\n', '|').strip()  # Last cell is rank, supports 2 or 3 cells

                            all_data.append({
                                'Serial No.': serial_number,
                                'College Name': college_name,
                                'Ranking Agency': ranking_agency,
                                'Year': year,
                                'Rank': rank
                            })

                    print(f"Scraped ranking data for {college_name} ({count}) from standard table")
                else:
                    print(f"Standard ranking table not found for {college_name} ({count})")
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Ranking Agency': "No data found",
                        'Year': "No data found",
                        'Rank': "No data found"
                    })

            except Exception:
                # If "Read More" button is not found, use the alternative table directly
                try:
                    table = driver.find_element(By.XPATH, '//table[@class="jsx-2440100204 table-new text-left mb-0"]')
                    print(f"Found special ranking table for {college_name}")

                    # Extract headers (years)
                    header_cells = table.find_elements(By.XPATH, './/tbody/tr/th/span')
                    years = [cell.text.strip() for cell in header_cells[1:]]  # Skip first column (Ranking Agency)

                    # Extract rows
                    rows = table.find_elements(By.XPATH, './/tr[@class="jsx-2440100204 tr"]')
                    for row in rows:
                        cells = row.find_elements(By.XPATH, './td')
                        ranking_agency = cells[0].text.replace('\n', ' ').strip()
                        ranking_agency = re.sub(r'(?i)\bcompare\b', '', ranking_agency).strip()
                        # Handle each year's rank
                        for i in range(1, len(cells)):
                                rank = cells[i].text.replace('\n', '|').strip()
                                
                                # Ensure we only access year if it exists
                                year = years[i - 1] if i - 1 < len(years) else "No data found"

                                all_data.append({
                                    'Serial No.': serial_number,
                                    'College Name': college_name,
                                    'Ranking Agency': ranking_agency,
                                    'Year': year,
                                    'Rank': rank
                                })
                    print(f"Scraped ranking data for {college_name} ({count}) from special table")
                except Exception as e:
                    print(f"Error finding special ranking table for {college_name}")
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Ranking Agency': "No data found",
                        'Year': "No data found",
                        'Rank': "No data found"
                    })

        except Exception as e:
            print(f"Ranking tab not found for {college_name} ({count})")
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Ranking Agency': "No data found",
                'Year': "No data found",
                'Rank': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count})")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Ranking Agency': "No data found",
            'Year': "No data found",
            'Rank': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\ranking_data_1000.csv", index=False)

# Close the browser
driver.quit()
