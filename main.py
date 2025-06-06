from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import uvicorn
import requests
import logging
import asyncio
import json
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
                # 🛡 Timeout protection: allow up to 500 seconds
copied_text = await loop.run_in_executor(None, run_scrape, email, password, url)            except asyncio.TimeoutError:
                logging.error(f"⏱ Scraping timed out for {email}")
                return

            if not copied_text:
                logging.error(f"❌ No link was returned for {FUB_email}. Skipping webhook.")
                return

            logging.info(f"✅ Scrape completed for {FUB_email}. Copied link: {copied_text}")

            send_webhook({
                "copied_text": copied_text,
                "FUB_ID": FUB_ID,
                "FUB_email": FUB_email
            })

    except Exception as error:
        logging.error(f"❌ Scraping failed for {FUB_email}: {type(error).__name__} – {error}")

def send_webhook(response):
    logging.info(f"📤 Sending webhook to {response_webhook_url}")
    logging.info(f"📦 Payload: {json.dumps(response)}")
    try:
        res = requests.post(response_webhook_url, json=response, timeout=10)
        if res.ok:
            logging.info("✅ Webhook was successful")
        else:
            logging.warning("⚠️ Webhook failed. Retrying once...")
            res_retry = requests.post(response_webhook_url, json=response, timeout=10)
            if res_retry.ok:
                logging.info("✅ Retry succeeded")
            else:
                logging.error(f"❌ Retry also failed. Status: {res_retry.status_code}")
                logging.error(res_retry.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Webhook exception: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
