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

        # Click on the Reviews button
        try:
            reviews_button = driver.find_element(By.XPATH, '//a[@data-ga-title="Reviews"]')
            reviews_button.click()
            time.sleep(2)  # Wait for the reviews page to load

            # Initialize placeholders for data
            rating = "no rating found"
            pros = []
            cons = []

            # Scrape the rating
            try:
                rating_element = driver.find_element(By.XPATH, '//span[@class="jsx-3895350182 mr-3"]')
                rating = rating_element.text.strip() if rating_element else "no rating found"
            except Exception as e:
                print(f"Rating not found for {college_name}: {e}")

            # Scrape the pros (limit to first 3)
            try:
                pros_elements = driver.find_elements(By.XPATH, '//*[@id="likes-dislikes"]/ul/li')
                for i, element in enumerate(pros_elements[:3]):  # Limit to first 3
                    pros.append(element.text.strip())
            except Exception as e:
                print(f"Pros not found for {college_name}: {e}")

            # Scrape the cons from either of the two XPaths
            cons_found = False  # Flag to check if cons are found
            for xpath in [
                '//*[@id="__next"]/div[2]/section/div[1]/div[3]/div/section/div[1]/section/div/div[2]/ul/li',
                '//*[@id="__next"]/div[2]/section/div[1]/div[2]/div/section/div[1]/section/div/div[2]/ul/li',
                '//*[@id="reviews"]/div[3]/section/section[1]/div[3]/section/div/div[2]/ul/li'
            ]:
                try:
                    cons_elements = driver.find_elements(By.XPATH, xpath)
                    if cons_elements:  # If elements are found, add to cons
                        cons = [element.text.strip() for element in cons_elements if element.text.strip()]
                        cons_found = True
                        break  # Exit the loop once we find the first valid cons
                except Exception as e:
                    print(f"Cons not found at XPath {xpath} for {college_name}: {e}")

            # Append the result to all_data list
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Rating': rating,
                'Pros': " | ".join(pros) if pros else "no pros found",
                'Cons': " | ".join(cons) if cons_found else "no cons found"
            })

            # Debug message indicating that data for the college has been scraped
            print(f"Scraped reviews for {college_name} ({counter})")

        except Exception as e:
            print(f"Reviews button not found for {college_name}: {e}")
            # Append empty data if reviews page was not accessible
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Rating': "no rating found",
                'Pros': "no pros found",
                'Cons': "no cons found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url}: {e}")
    counter += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file named reviews_50sample.csv
scraped_df.to_csv("DATA\\reviews_1000.csv", index=False)

# Close the browser
driver.quit()
