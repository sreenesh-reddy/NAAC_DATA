from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Path to your ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Open the NAAC website
url = "https://assessmentonline.naac.gov.in/public/index.php/hei_dashboard"
driver.get(url)

# Wait for the category dropdown
wait = WebDriverWait(driver, 10)
try:
    # Select "PTR Submitted" from the "A & A Status" dropdown
    aa_status_dropdown = wait.until(EC.presence_of_element_located((By.ID, "iiqa_status")))
    select = Select(aa_status_dropdown)
    select.select_by_visible_text("SSR Submitted")
    time.sleep(1)  # Short pause to ensure selection registers

    # Click the "Show Details" button using JavaScript
    show_details_button = driver.find_element(By.ID, "showbtn")
    driver.execute_script("arguments[0].click();", show_details_button)
    print("Clicked 'Show Details' button, waiting for table to load...")

    # Wait for the table to load and ensure at least one row appears
    wait.until(EC.presence_of_element_located((By.ID, "details_table")))
    rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#details_table tbody tr")))
    print(f"Table loaded successfully! Found {len(rows)} rows on the first page.")

    college_names = []

    # Function to extract college names
    def extract_college_names():
        rows = driver.find_elements(By.XPATH, '//table[@id="details_table"]/tbody/tr')
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 1:  # Ensure valid row
                college_name = cols[1].text.strip()
                if college_name:
                    college_names.append(college_name)

    # Extract names from the first page
    extract_college_names()

    # Loop through pages
    while True:
        try:
            next_button = driver.find_element(By.ID, "details_table_next")
            if "disabled" in next_button.get_attribute("class"):
                print("Reached the last page.")
                break
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(3)  # Allow time for new data to load
            extract_college_names()
        except:
            break

    # Save to a text file
    with open("college_names.txt", "w", encoding="utf-8") as f:
        for name in college_names:
            f.write(name + "\n")

    print(f"Scraped {len(college_names)} college names and saved to 'college_names.txt'.")

except Exception as e:
    print(f"An error occurred during extraction: {e}")

finally:
    driver.quit()
