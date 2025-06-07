import json
import requests
import os
from datetime import datetime

FAILED_FILE = "/root/stars-web-scrape/failed_webhooks.jsonl"
RETRY_LOG = "/root/stars-web-scrape/retry_log.jsonl"
WEBHOOK_URL = "https://hook.integrator.boost.space/k80rinp9fgzwhlysiohlvy12x8r0qa36"

def load_failed_webhooks():
    if not os.path.exists(FAILED_FILE):
        return []

    with open(FAILED_FILE, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def write_failed_webhooks(data):
    with open(FAILED_FILE, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")

def log_retry_attempt(payload, success, message):
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "payload": payload,
        "status": "success" if success else "failed",
        "message": message
    }
    with open(RETRY_LOG, "a") as f:
        f.write(json.dumps(log_entry) + "\n")

def retry_failed_webhooks():
    queue = load_failed_webhooks()
    if not queue:
        print("✅ No failed webhooks to retry.")
        return

    still_failed = []

    for entry in queue:
        payload = entry["payload"]
        try:
            res = requests.post(WEBHOOK_URL, json=payload, timeout=10)
            if res.ok:
                print(f"✅ Retry success for: {payload.get('FUB_email')}")
                log_retry_attempt(payload, True, "Retry succeeded")
            else:
                print(f"❌ Retry failed for: {payload.get('FUB_email')} — {res.status_code}")
                entry["error"] = f"HTTP {res.status_code}"
                still_failed.append(entry)
                log_retry_attempt(payload, False, res.text)
        except Exception as e:
            print(f"❌ Exception during retry for: {payload.get('FUB_email')} — {e}")
            entry["error"] = str(e)
            still_failed.append(entry)
            log_retry_attempt(payload, False, str(e))

    write_failed_webhooks(still_failed)
    print(f"🔁 Retry complete. Remaining in queue: {len(still_failed)}")

if __name__ == "__main__":
    retry_failed_webhooks()
