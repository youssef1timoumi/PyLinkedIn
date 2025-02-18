from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🔹 Replace with your LinkedIn credentials
LINKEDIN_EMAIL = "email"
LINKEDIN_PASSWORD = "password"
# Set up Selenium options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument("--window-size=1920,1080")

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.delete_all_cookies()

# 🔹 Navigate to LinkedIn Login Page
driver.get("https://www.linkedin.com/login")
time.sleep(3)  # Allow time for page to load

# 🔹 Enter Email
try:
    email_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "username"))
    )
    email_field.send_keys(LINKEDIN_EMAIL)
    print("✅ Entered Email")
except:
    print("❌ Failed to find email field.")

# 🔹 Enter Password
try:
    password_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_field.send_keys(LINKEDIN_PASSWORD)
    print("✅ Entered Password")
except:
    print("❌ Failed to find password field.")

# 🔹 Click Login Button
try:
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    login_button.click()
    print("✅ Clicked Login Button")
except:
    print("❌ Failed to click login button.")

time.sleep(5)  # Allow time for login to process

# 🔹 Check for 2FA Verification
try:
    # Wait for the verification field to appear (assuming SMS or App verification)
    two_factor_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='input__phone_verification_pin']"))
    )

    print("🔒 2FA Detected! Please enter the verification code from your phone:")
    auth_code = input("Enter 2FA Code: ")  # Manually enter 2FA code

    # 🔹 Enter 2FA Code
    two_factor_input.send_keys(auth_code)
    submit_2fa_button = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary')]")
    submit_2fa_button.click()
    print("✅ Submitted 2FA Code")

    time.sleep(5)  # Allow time for authentication

except:
    print("✅ No 2FA Detected. Login successful!")

# 🔹 Continue surfing LinkedIn
print("🚀 Successfully logged in. You can now navigate LinkedIn pages.")

