import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Load job titles from CSV file
data = pd.read_csv("filtered_engineering_jobs.csv")
job_titles = data["Alternate Title"].dropna().unique()

# Initialize WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 2)

# Open Glassdoor Salaries page
driver.get("https://www.glassdoor.co.in/Salaries/index.htm")

def handle_login():
    """Handles login popup if it appears."""
    try:
        email_input = wait.until(EC.presence_of_element_located((By.ID, "hardsellUserEmail")))
        email_input.send_keys("your_email@example.com")
        email_input.send_keys(Keys.RETURN)
        
        password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_input.send_keys("your_password")
        password_input.send_keys(Keys.RETURN)
        
        print("Logged in successfully ✅")
    except TimeoutException:
        print("No login popup appeared. Skipping login.")

# Handle login if popup appears

results = []

for title in job_titles:
    try:
        driver.get("https://www.glassdoor.co.in/Salaries/index.htm")
        
        # Wait for job title input box and enter job title
        job_title_box = wait.until(EC.presence_of_element_located((By.ID, "job-title-autocomplete")))
        job_title_box.clear()
        job_title_box.send_keys(title)

        # Wait for location input box and enter "India"
        location_box = wait.until(EC.presence_of_element_located((By.ID, "location-autocomplete")))
        location_box.clear()
        location_box.send_keys("India")

        # Wait for the search button and click it
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test='desktop-submit-button']")))
        search_button.click()

        # Capture the initial search page URL
        time.sleep(2)
        initial_page_link = driver.current_url

        # Check if "No current reports" message exists
        try:
            

            # Try to extract salary range if no "No current reports" message
            salary_range_element = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@data-test='total-pay']//span[contains(@class,'TotalPayRange_StyledAverageBasePay')]")))
            salary_range = salary_range_element.text
            if not salary_range_element:
                no_salary_element = driver.find_elements(By.XPATH, "//section[@data-test='hero-wrapper-module']//h1")
                
                if no_salary_element:
                    # Extract text from h1 and check if it actually says "No current reports"
                    no_salary_text = no_salary_element[0].text.lower()
                    if "no current reports" in no_salary_text:
                        salary_range = "NA"
                    else:
                        raise Exception("Salary data likely exists, but failed to extract.")  
                else:
                    raise Exception("Salary section not found.")
        except (TimeoutException, NoSuchElementException):
            salary_range = "NA"

        print(salary_range)


        # Store results with "All years" as experience level
        results.append([title, "India", "All years", salary_range])

    except Exception as e:
        print(f"Error processing job title {title}: {e}")

# Save results to CSV
output_df = pd.DataFrame(results, columns=["Job Title", "Location", "Experience", "Salary Range"])
output_df.to_csv("scraped_salaries.csv", index=False)

# Close the browser
driver.quit()
print("✅ Scraping completed. Data saved to scraped_salaries.csv")
