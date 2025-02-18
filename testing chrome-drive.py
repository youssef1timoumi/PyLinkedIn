from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.delete_all_cookies()

# LinkedIn job search URL
url = "https://www.linkedin.com/jobs/search?keywords=Devops&location=Tunisia&geoId=&position=1&pageNum=0"

# Load the job search page
driver.get(url)
time.sleep(5)  # Allow JavaScript to load

try:
    # Extract the first job link
    first_job = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'base-card__full-link')]"))
    )
    job_link = first_job.get_attribute("href")
    print(f"🔗 First Job Link: {job_link}")

    # Navigate to the job posting
    driver.get(job_link)
    time.sleep(5)  # Allow the job page to load

    # Handle LinkedIn login popup if it appears
    try:
        close_popup_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Dismiss')]"))
        )
        close_popup_button.click()
        print("🔒 Detected login popup and closed it.")
        time.sleep(2)  # Allow page update
    except:
        print("✅ No login popup detected.")

    # Click the "Save" or "Apply" button even if it has no direct link
    try:
        apply_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'jobs-apply-button')]"))
        )
        apply_button.click()
        print("✅ Clicked the 'Apply' button successfully!")

        # Wait for popup to appear
        time.sleep(3)

        # If a form appears after clicking, print confirmation
        try:
            form_popup = driver.find_element(By.XPATH, "//div[contains(@class, 'jobs-easy-apply-modal')]")
            print("✅ The application form popup is now open!")
        except:
            print("⚠️ No application form detected after clicking the button.")

    except Exception as e:
        print("❌ No 'Apply' button found or not clickable.", e)

except Exception as e:
    print("❌ No job postings found.", e)

# Close the browser
driver.quit()
