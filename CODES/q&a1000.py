from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
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

        # Try to click the Q&A button
        try:
            qa_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Q&A"]')
            qa_tab.click()
            time.sleep(2)  # Wait for the page to load after clicking
        except:
            # Click the arrow button to reveal more options if the Q&A button is not visible
            try:
                arrow_button = driver.find_element(By.XPATH, '//div[@class="jsx-3207461571 right-arrow d-flex flex-column justify-content-center pointer arrow position-absolute d-block bg-white rounded"]')
                arrow_button.click()
                time.sleep(1)
                qa_tab = driver.find_element(By.XPATH, '//a[@data-ga-title="Q&A"]')
                qa_tab.click()
                time.sleep(2)
            except:
                print(f"Q&A tab not found for {college_name} ({count})")
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Question': "No data found",
                    'Answer': "No data found"
                })
                count += 1
                continue

        # Locate and click "Read More" buttons for expanding answers
        read_more_buttons = driver.find_elements(By.XPATH, '//span[@data-test-id="ques-read-more"]')
        for button in read_more_buttons:
            try:
                ActionChains(driver).move_to_element(button).click().perform()
            except Exception as e:
                print(f"Error clicking 'Read More' button: {e}")

        # Extract questions
        questions = driver.find_elements(By.XPATH, '//a[@class="jsx-124254234 jsx-1484856324 text-dark"]')

        # Try to find answers from the primary xpath
        answers = driver.find_elements(By.XPATH, '//div[@class="cdcms_college_highlights"]')
        
        # If primary answers are not found, check alternative locations
        if not answers:
            answers = driver.find_elements(By.XPATH, '//div[@class="cdcms_courses"]')
        if not answers:
            answers = driver.find_elements(By.XPATH, '//div[@class="cdcms_comparison"]')
        if not answers:
            answers = driver.find_elements(By.XPATH, '//div[@class="cdcms_admission_highlights"]')

        max_data = min(10, len(questions), len(answers))  # Get the minimum between 10 and the number of available questions/answers

        if max_data > 0:
            for i in range(max_data):
                question_text = questions[i].text.strip() if questions[i].text else "No question text"
                answer_text = answers[i].text.strip() if i < len(answers) and answers[i].text else "No answer text"

                # Append the data to the list
                all_data.append({
                    'Serial No.': serial_number,
                    'College Name': college_name,
                    'Question': question_text,
                    'Answer': answer_text
                })

            print(f"Scraped Q&A for {college_name} ({count})")
        else:
            # No Q&A data found
            all_data.append({
                'Serial No.': serial_number,
                'College Name': college_name,
                'Question': "No data found",
                'Answer': "No data found"
            })
            print(f"No Q&A data found for {college_name} ({count})")

    except Exception as e:
        print(f"Error processing {college_name} at {college_url} ({count}): {e}")
        all_data.append({
            'Serial No.': serial_number,
            'College Name': college_name,
            'Question': "No data found",
            'Answer': "No data found"
        })

    count += 1

# Convert the scraped data into a DataFrame
scraped_df = pd.DataFrame(all_data)

# Export the data to a CSV file
scraped_df.to_csv("DATA\\qa_data_1000.csv", index=False)

# Close the browser
driver.quit()
