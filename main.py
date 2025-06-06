from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, EmailStr
import uvicorn
import requests
import concurrent.futures
from scrape import run_scrape

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
    background_tasks.add_task(
        run_scrape_and_send_webhook,
        user_credential.email,
        user_credential.password,
        user_credential.url,
        user_credential.FUB_ID,
        user_credential.FUB_email
    )
    return {'message': f'Scraping in progress. Check webhook for results. 👉 {resonse_webhook_url}'}

async def run_scrape_and_send_webhook(email: EmailStr, password: str, url: str, FUB_ID: int, FUB_email: EmailStr):
    try:
        print('____started scraping script____')

        # Run scrape with 90-second timeout
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(run_scrape, email, password, url)
            copied_text = future.result(timeout=90)  # Timeout protection

        # Send result to webhook
        send_webhook({
            "copied_text": copied_text,
            "FUB_ID": FUB_ID,
            "FUB_email": FUB_email
        })

    except concurrent.futures.TimeoutError:
        print(f"⏱ Scraping timed out for {email}")

    except Exception as error:
        print(f"❌ An error occurred: {type(error).__name__} – {error}")

def send_webhook(response):
    print('📤 Sending webhook response...')
    print(response)
    try:
        res = requests.post(resonse_webhook_url, json=response, timeout=10)
        if res.ok:
            print('✅ Webhook was successful')
        else:
            print('⚠️ Webhook failed. Retrying once...')
            res_retry = requests.post(resonse_webhook_url, json=response, timeout=10)
            if res_retry.ok:
                print('✅ Retry succeeded')
            else:
                print(f"❌ Retry also failed. Status: {res_retry.status_code}")
                print('Response:', res_retry.text)
    except requests.exceptions.RequestException as e:
        print('❌ Webhook exception:', e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
