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

        # Try to click the News & Articles button
        try:
            news_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="News & Articles"]')
            news_tab.click()
            time.sleep(2)  # Wait for the page to load after clicking
        except:
            # Click the arrow button to reveal more options if the News & Articles button is not visible
            try:
                arrow_button = driver.find_element(By.XPATH, '//div[@class="jsx-3207461571 right-arrow d-flex flex-column justify-content-center pointer arrow position-absolute d-block bg-white rounded"]')
                arrow_button.click()
                time.sleep(1)
                news_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="News & Articles"]')
                news_tab.click()
                time.sleep(2)
            except:
                print(f"News & Articles tab not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Title': "No data found",
                    'Link': "No data found"
                })
                count += 1
                continue

        # Extract news and article data
        articles = driver.find_elements(By.XPATH, '//a[@class="jsx-3082775996 news-title fs-16 text-primary-black font-weight-semi "]')

        if articles:
            # Limit to a maximum of 10 articles
            articles = articles[:10]
            for article in articles:
                title = article.text.strip()
                href = article.get_attribute('href')
                full_link = f"{href}" if href else "No data found"

                # Append the data to the list
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Title': title,
                    'Link': full_link
                })

            print(f"Scraped up to 10 news & articles for {college_name} ({count})")
        else:
            # No news data found
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Title': "No data found",
                'Link': "No data found"
            })
            print(f"No news & articles data found for {college_name} ({count})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count}): {e}")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Title': "No data found",
            'Link': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\news_articles_data_1000.csv", index=False)

# Close the browser
driver.quit()
