from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import uvicorn
import requests
import concurrent.futures
import logging
from scrape import run_scrape

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = FastAPI()
resonse_webhook_url = "https://hook.integrator.boost.space/k80rinp9fgzwhlysiohlvy12x8r0qa36"

class UserCredential(BaseModel):
    email: EmailStr
    password: str
    url: str
    FUB_ID: int
    FUB_email: EmailStr

@app.post("/")
async def main(user_credential: UserCredential, background_tasks: BackgroundTasks):
    logging.info("📬 Received POST / request")
    background_tasks.add_task(
        run_scrape_and_send_webhook,
        user_credential.email,
        user_credential.password,
        user_credential.url,
        user_credential.FUB_ID,
        user_credential.FUB_email
    )
    return {'message': f'Scraping in progress. Check webhook for results. 👉 {resonse_webhook_url}'}

@app.get("/health")
async def health():
    return {"status": "ok"}

async def run_scrape_and_send_webhook(email: EmailStr, password: str, url: str, FUB_ID: int, FUB_email: EmailStr):
    try:
        logging.info("🔥 Started scraping script")

        # Run scrape with 90-second timeout
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_scrape, email, password, url)
            copied_text = future.result(timeout=90)

        # Send result to webhook
        send_webhook({
            "copied_text": copied_text,
            "FUB_ID": FUB_ID,
            "FUB_email": FUB_email
        })

    except concurrent.futures.TimeoutError:
        logging.error(f"⏱ Scraping timed out for {email}")
    except Exception as error:
        logging.error(f"❌ An error occurred: {type(error).__name__} – {error}")

def send_webhook(response):
    logging.info("📤 Sending webhook response...")
    logging.info(response)
    try:
        res = requests.post(resonse_webhook_url, json=response, timeout=10)
        if res.ok:
            logging.info("✅ Webhook was successful")
        else:
            logging.warning("⚠️ Webhook failed. Retrying once...")
            res_retry = requests.post(resonse_webhook_url, json=response, timeout=10)
            if res_retry.ok:
                logging.info("✅ Retry succeeded")
            else:
                logging.error(f"❌ Retry also failed. Status: {res_retry.status_code}")
                logging.error(res_retry.text)
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Webhook exception: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
