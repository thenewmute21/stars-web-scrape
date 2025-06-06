from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
import time
import logging

api_key = "YOUR_2CAPTCHA_API_KEY"
SITE_KEY = "6LezG3omAAAAAGrXICTuXz0ueeMFIodySqJDboLT"  # ✅ Replace with real site key
base_url = "https://stars.ylopo.com/auth"

# Enable logging with timestamp
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def run_scrape(email, password, website_url):
    logging.info(f"🌐 Starting scraping for {email}")
    driver = webdriver.Chrome(options=options)
    driver.get(website_url)

    try:
        email_elem = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
        email_elem.clear()
        email_elem.send_keys(email)

        password_elem = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
        password_elem.clear()
        password_elem.send_keys(password)

        logging.info("🔐 Solving Captcha...")
        solver = TwoCaptcha(api_key)
        response = solver.recaptcha(sitekey=SITE_KEY, url=base_url)
        code = response['code']
        logging.info("✅ Captcha solved")

        # Inject the token
        driver.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
        recaptcha_text_area = driver.find_element(By.ID, "g-recaptcha-response")
        recaptcha_text_area.clear()
        recaptcha_text_area.send_keys(code)

        # Submit login
        login_btn = driver.find_element(By.CLASS_NAME, "pb-button")
        login_btn.send_keys(Keys.RETURN)
        logging.info("✅ Successfully submitted login")

        # Wait for .ylopo-button to appear
        max_wait_seconds = 120
        poll_interval = 1
        elapsed = 0
        link_btn = None

        while elapsed < max_wait_seconds:
            try:
                link_btn = driver.find_element(By.CLASS_NAME, 'ylopo-button')
                break
            except:
                time.sleep(poll_interval)
                elapsed += poll_interval

        if not link_btn:
            logging.error("❌ Timed out waiting for .ylopo-button to appear.")
            driver.quit()
            return None

        logging.info("✅ Ylopo dashboard loaded")
        current_url = driver.current_url
        logging.info(f"📍 Current URL: {current_url}")
        url_slug = current_url.split('/')[-1]

        # Fetch user/search info
        user_info_script = f"""
        return fetch("https://stars.ylopo.com/api/1.0/open/{url_slug}?includes[]=allSavedSearches.searchAlerts.valuationReport")
            .then(response => response.json())
            .then(data => {{
                const userId = data.id;
                const searchId = data.buyerSavedSearches?.[0]?.id || null;
                return [userId, searchId];
            }})
            .catch(error => {{
                console.error('Error:', error);
                return null;
            }});
        """
        user_info = driver.execute_script(user_info_script)

        if not user_info or not user_info[0] or not user_info[1]:
            logging.error(f"❌ Missing user_id or search_id: {user_info}")
            driver.quit()
            return None

        user_id, search_id = user_info
        logging.info(f"🆔 user_id: {user_id}, search_id: {search_id}")

        # Fetch short link
        copied_link_script = f"""
        const callback = arguments[0];
        fetch("https://stars.ylopo.com/api/1.0/lead/{user_id}/encryptedLink?personId={user_id}&runSearch=true&savedSearchId={search_id}")
            .then(response => response.json())
            .then(data => {{
                if (data.shortLink) {{
                    callback(data.shortLink);
                }} else {{
                    console.error("No shortLink found");
                    callback(null);
                }}
            }})
            .catch(error => {{
                console.error('Link fetch error:', error);
                callback(null);
            }});
        """
        copied_link = driver.execute_async_script(copied_link_script)

        if copied_link:
            logging.info(f"🔗 Copied link: {copied_link}")
        else:
            logging.error("❌ No copied link returned")

        return copied_link

    except Exception as e:
        logging.error(f"❌ Exception in run_scrape(): {type(e).__name__} — {e}")
        return None

    finally:
        driver.quit()
        logging.info("🧹 Browser session closed")
