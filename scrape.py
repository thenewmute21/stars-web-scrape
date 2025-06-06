from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from twocaptcha import TwoCaptcha
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time
import json

SITE_KEY = '6LezG3omAAAAAGrXICTuXz0ueeMFIodySqJDboLT'
api_key = '147f2a193a2db639a49c64a00ed66cd5'
base_url = 'https://stars.ylopo.com/auth'

# Create Chrome options for headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
# options.add_argument("--log-level=DEBUG")
options.add_experimental_option(
    "prefs", {
        # block image loading
        "profile.managed_default_content_settings.images": 2,
    }
)

def run_scrape(email, password, website_url):
    driver = webdriver.Chrome(options=options)
    driver.get(website_url)

    # input email in email field
    email_elem = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
    email_elem.clear()
    email_elem.send_keys(email)

    # input passowrd in password field
    password_elem = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
    password_elem.clear()
    password_elem.send_keys(password)


    # by-pass recapcha
    print("Solving Captcha")
    solver = TwoCaptcha(api_key)
    response = solver.recaptcha(sitekey=SITE_KEY, url=base_url)
    code = response['code']
    print(f"Successfully solved the Captcha. The solve code is {code}")

    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
    recaptcha_text_area = driver.find_element(By.ID, "g-recaptcha-response")
    recaptcha_text_area.clear()
    recaptcha_text_area.send_keys(code)

    # click the login button
    login_btn = driver.find_element(By.CLASS_NAME, "pb-button")
    login_btn.send_keys(Keys.RETURN)
    print('successfully logged in')

    # wait for second page to load and button found
    link_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ylopo-button'))
    )
    # Retrieve the copied text from the clipboard using pyperclip


    # Get user id and search id
    print(driver.current_url)
    url_slug = driver.current_url.split('/')[-1]
    print('url_slug: ', url_slug)

    get_user_info_script = f"""
    return fetch("https://stars.ylopo.com/api/1.0/open/{url_slug}?includes[]=allSavedSearches.searchAlerts.valuationReport")
        .then(response => response.json())
        .then(data => {{
            const userId = data.id;
            const searchId = data.buyerSavedSearches && data.buyerSavedSearches.length > 0 
                ? data.buyerSavedSearches[0].id 
                : null;
            return [userId, searchId];
        }})
        .catch(error => {{
            console.error('Error:', error);
            return null;
        }});
    """
    user_info = driver.execute_script(get_user_info_script)

    if user_info:
        user_id, search_id = user_info
        print(f"user_id: {user_id}, search_id: {search_id}")
    else:
        print("Failed to retrieve user information.")


    # Execute JavaScript to send the request from the webpage and store the copied link in a variable
    copied_link_script = f"""
    return fetch("https://stars.ylopo.com/api/1.0/lead/{user_id}/encryptedLink?personId={user_id}&runSearch=true&savedSearchId={search_id}")
        .then(response => response.json())
        .then(data => data.shortLink)
        .catch(error => console.error('Error:', error));
    """
    copied_link = driver.execute_script("return (function() { " + copied_link_script + " })()")

    print("Copied link:", copied_link)

    driver.close()

    return copied_link
