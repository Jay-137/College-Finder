from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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

        # Click on the Gallery tab
        try:
            gallery_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Gallery"]')
            gallery_tab.click()
            
            # Wait for the images to load (adjust the wait condition as necessary)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"gallery-new")]//img'))
            )
            time.sleep(2)  # Additional wait for images to load fully

            # Locate the image elements
            image_elements = driver.find_elements(By.XPATH, '//div[contains(@class,"gallery-new")]//img')

            if image_elements:
                # Limit to the first 30 images
                max_images = min(len(image_elements), 30)
                for i in range(max_images):
                    img_src = image_elements[i].get_attribute('src')  # Get the source of the image

                    # Check if img_src is a Data URI and try other attributes
                    if img_src.startswith('data:image'):
                        # Try to get other attributes that might hold the original URL
                        img_src = image_elements[i].get_attribute('data-src') or image_elements[i].get_attribute('data-original') or "Data URI (Filtered out)"
                    
                    all_data.append({
                        'Serial No.': serial_number,
                        'College Name': college_name,
                        'Image Source': img_src
                    })
                print(f"Scraped {max_images} images for {college_name} ({count})")
            else:
                # If no images found
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Image Source': "No data found"
                })
                print(f"No images found for {college_name} ({count})")

        except Exception as e:
            print(f"Gallery tab not found for {college_name} ({count})")
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Image Source': "No data found"
            })

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count})")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Image Source': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\gallery_data_1000.csv", index=False)

# Close the browser
driver.quit()
