from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import uvicorn
import requests
import logging
import asyncio
import json
from datetime import datetime
from scrape import run_scrape

# Logging setup — write to file and terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("/root/stars-web-scrape/log.txt"),
        logging.StreamHandler()
    ]
)

app = FastAPI()
response_webhook_url = "https://hook.integrator.boost.space/k80rinp9fgzwhlysiohlvy12x8r0qa36"

# Limit to 2 concurrent scrapes globally
semaphore = asyncio.Semaphore(2)

class UserCredential(BaseModel):
    email: EmailStr
    password: str
    url: str
    FUB_ID: int
    FUB_email: EmailStr

@app.post("/")
async def main(user_credential: UserCredential, background_tasks: BackgroundTasks):
    logging.info(f"📬 Received POST request for {user_credential.FUB_email} (FUB_ID: {user_credential.FUB_ID})")
    background_tasks.add_task(
        run_scrape_and_send_webhook,
        user_credential.email,
        user_credential.password,
        user_credential.url,
        user_credential.FUB_ID,
        user_credential.FUB_email
    )
    return {'message': f'Scraping in progress. Check webhook for results. 👉 {response_webhook_url}'}

@app.get("/health")
async def health():
    return {"status": "ok"}

async def run_scrape_and_send_webhook(email: EmailStr, password: str, url: str, FUB_ID: int, FUB_email: EmailStr):
    try:
        async with semaphore:
            logging.info(f"🔥 Started scraping script for {FUB_email} — URL: {url}")
            loop = asyncio.get_event_loop()

            try:
                copied_text = await loop.run_in_executor(None, run_scrape, email, password, url)
            except Exception as scrape_err:
                logging.error(f"❌ Scraping threw an error for {FUB_email}: {scrape_err}")
                return

            if not copied_text:
                logging.error(f"❌ No link was returned for {FUB_email}. Skipping webhook.")
                return

            logging.info(f"✅ Scrape completed for {FUB_email}. Copied link: {copied_text}")

            payload = {
                "copied_text": copied_text,
                "FUB_ID": FUB_ID,
                "FUB_email": FUB_email,
                "timestamp": datetime.utcnow().isoformat()
            }

            # Save success locally
            try:
                with open("/root/stars-web-scrape/scraped_log.jsonl", "a") as logf:
                    logf.write(json.dumps(payload) + "\n")
            except Exception as log_error:
                logging.warning(f"⚠️ Failed to log scrape result: {log_error}")

            send_webhook(payload)

    except Exception as error:
        logging.error(f"❌ Scraping failed for {FUB_email}: {type(error).__name__} – {error}")

def send_webhook(response):
    logging.info(f"📤 Sending webhook to {response_webhook_url}")
    logging.info(f"📦 Payload: {json.dumps(response)}")
    try:
        res = requests.post(response_webhook_url, json=response, timeout=10)
        logging.info(f"🔄 Webhook response status: {res.status_code}")
        logging.info(f"📨 Webhook response body: {res.text}")

        if res.ok:
            logging.info("✅ Webhook was successful")
        else:
            logging.warning("⚠️ Webhook failed. Retrying once...")
            res_retry = requests.post(response_webhook_url, json=response, timeout=10)
            logging.info(f"🔁 Retry response status: {res_retry.status_code}")
            logging.info(f"🔁 Retry response body: {res_retry.text}")
            if res_retry.ok:
                logging.info("✅ Retry succeeded")
            else:
                logging.error(f"❌ Retry also failed. Status: {res_retry.status_code}")
                save_failed_webhook(response, f"Retry failed with status {res_retry.status_code}")
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Webhook exception: {e}")
        save_failed_webhook(response, str(e))

def save_failed_webhook(response, error_message):
    try:
        failed_record = {
            "payload": response,
            "error": error_message,
            "failed_at": datetime.utcnow().isoformat()
        }
        with open("/root/stars-web-scrape/failed_webhooks.jsonl", "a") as f:
            f.write(json.dumps(failed_record) + "\n")
        logging.info("📝 Saved failed webhook to retry queue")
    except Exception as e:
        logging.error(f"❌ Failed to write to failed_webhooks.jsonl: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=600)
