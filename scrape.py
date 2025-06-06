from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twocaptcha import TwoCaptcha
import time

api_key = "YOUR_2CAPTCHA_API_KEY"
SITE_KEY = "6LezG3omAAAAAGrXICTuXz0ueeMFIodySqJDboLT"  # Replace with real site key
base_url = "https://stars.ylopo.com/auth"

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

def run_scrape(email, password, website_url):
    driver = webdriver.Chrome(options=options)
    driver.get(website_url)

    email_elem = driver.find_element(By.CSS_SELECTOR, "input[type=text]")
    email_elem.clear()
    email_elem.send_keys(email)

    password_elem = driver.find_element(By.CSS_SELECTOR, "input[type=password]")
    password_elem.clear()
    password_elem.send_keys(password)

    print("Solving Captcha")
    solver = TwoCaptcha(api_key)
    response = solver.recaptcha(sitekey=SITE_KEY, url=base_url)
    code = response['code']
    print(f"Successfully solved the Captcha. The solve code is {code}")

    driver.execute_script("document.getElementById('g-recaptcha-response').style.display = '';")
    recaptcha_text_area = driver.find_element(By.ID, "g-recaptcha-response")
    recaptcha_text_area.clear()
    recaptcha_text_area.send_keys(code)

    login_btn = driver.find_element(By.CLASS_NAME, "pb-button")
    login_btn.send_keys(Keys.RETURN)
    print('successfully logged in')

    # 🛠️ Wait for login redirect and button
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
        print("❌ Timed out waiting for .ylopo-button to appear after 120 seconds.")
        driver.quit()
        raise TimeoutError("ylopo-button never appeared")

    print(driver.current_url)
    url_slug = driver.current_url.split('/')[-1]
    print('url_slug: ', url_slug)

    # Get user_id and search_id
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
        driver.quit()
        raise Exception("User info fetch failed")

    # ✅ Patch: use async script to return copied_link correctly and with fallback logging
    try:
        copied_link_script = f"""
        const callback = arguments[0];
        fetch("https://stars.ylopo.com/api/1.0/lead/{user_id}/encryptedLink?personId={user_id}&runSearch=true&savedSearchId={search_id}")
            .then(response => response.json())
            .then(data => {{
                if (data.shortLink) {{
                    callback(data.shortLink);
                }} else {{
                    console.error("No shortLink found in response.");
                    callback(null);
                }}
            }})
            .catch(error => {{
                console.error('Link fetch error:', error);
                callback(null);
            }});
        """
        copied_link = driver.execute_async_script(copied_link_script)
    except Exception as e:
        print(f"❌ Exception while fetching shortLink: {e}")
        copied_link = None

    if copied_link:
        print("Copied link:", copied_link)
    else:
        print("❌ No copied link returned.")

    driver.quit()
    return copied_link
