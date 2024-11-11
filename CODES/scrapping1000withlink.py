from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import csv

# Specify the website and path to chromedriver
website = 'https://collegedunia.com/btech/private-colleges'
path = "DATA\\chromedriver-win64\\chromedriver-win64\\chromedriver.exe"
# Create a Service object using the path
service = Service(path)

# Initialize the Chrome WebDriver
driver = webdriver.Chrome(service=service)

# Open the website
driver.get(website)

# Function to scroll the page
def scroll_down(driver):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(0.2)
# Initialize a list to store unique colleges with URLs while maintaining order
colleges_list = []

# Scroll until the 501st college is visible
while True:
    try:
        # Try to locate the 501st college using XPath with index [501]
        college_501 = driver.find_element(By.XPATH, '(//h3[@class="jsx-3230181281 font-weight-medium text-lg mb-0"])[501]')
        print(f"501st college found: {college_501.text}")
        break  # Exit the loop if the 501st college is found
    except:
        # If the 501st college is not yet loaded, scroll down
        scroll_down(driver)
        print("Scrolling down to load more colleges...")

# Now that the 501st college is visible, collect the next 500 unique colleges starting from the 501st one
while len(colleges_list) < 500:
    # Find all college elements (the <a> tags containing name and URL)
    college_elements = driver.find_elements(By.XPATH, '//a[@class="jsx-3230181281 college_name underline-on-hover"]')
    
    # Add colleges starting from the 501st onward to the list, avoiding duplicates
    for college in college_elements[500:]:  # Skip the first 500 colleges
        # Extract the college name and URL
        college_name_elem = college.find_element(By.TAG_NAME, 'h3')
        college_info = college_name_elem.text
        partial_url = college.get_attribute("href")
        
        # Construct the full URL by appending the base URL
        full_url = f"https://collegedunia.com{partial_url}" if partial_url.startswith('/') else partial_url
        
        # Split the college name and location at the last comma
        if ',' in college_info:
            name, location = college_info.rsplit(',', 1)
            name = name.strip()  # Remove any leading/trailing whitespace from the name
            location = location.strip()  # Remove any leading/trailing whitespace from the location
            college_tuple = (name, location, full_url)
        else:
            college_tuple = (college_info.strip(), "", full_url)  # In case there is no location
        
        # Add only if not already in the list to maintain order
        if college_tuple not in colleges_list:
            colleges_list.append(college_tuple)

    # Scroll to load more colleges if necessary
    scroll_down(driver)
    
    # Print progress
    print(f"Collected {len(colleges_list)} unique colleges from 501st onward...")

# Save the next 500 unique colleges (from 501st to 1000th) to a CSV file
with open('DATA\\next_500_colleges.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Serial No.', 'College Name', 'Location', 'URL'])  # Added 'URL' header

    for idx, (college_name, location, url) in enumerate(colleges_list, start=501):
        writer.writerow([idx, college_name, location, url])

# Close the driver after scraping
driver.quit()

print(f"Scraped colleges from 501 to 1000 and saved to 'next_500_colleges.csv'.")
