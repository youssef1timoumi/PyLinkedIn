from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
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
url = "https://www.linkedin.com/jobs/search?keywords=Devops&location=tunisia"
# Load the page
driver.get(url)
# Wait for JavaScript to load
time.sleep(5)  # Adjust if needed

# Get full page source
html_content = driver.page_source
driver.quit()  # Close the browser after fetching content

soup = BeautifulSoup(html_content, "html.parser")

# Extract job postings
job_cards = soup.find_all("div", class_="base-card")  # Adjust if necessary

# Extract and print job details
for i, job in enumerate(job_cards[:10]):  # Limit to first 10 jobs
    title = job.find("h3", class_="base-search-card__title").get_text(strip=True) if job.find("h3", class_="base-search-card__title") else "N/A"
    company = job.find("h4", class_="base-search-card__subtitle").get_text(strip=True) if job.find("h4", class_="base-search-card__subtitle") else "N/A"
    location = job.find("span", class_="job-search-card__location").get_text(strip=True) if job.find("span", class_="job-search-card__location") else "N/A"
    job_link = job.find("a", class_="base-card__full-link")["href"] if job.find("a", class_="base-card__full-link") else "N/A"

    print(f"📌 Job {i+1}:")
    print(f"   🏢 Company: {company}")
    print(f"   📍 Location: {location}")
    print(f"   🔗 Link: {job_link}")
    print("-" * 50)

