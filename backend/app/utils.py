import os
import requests

# Grab the URL from the .env file
#WEBHOOK_URL = os.environ.get("GOOGLE_SHEETS_WEBHOOK_URL")

WEBHOOK_URL ="https://script.google.com/a/macros/hitam.org/s/AKfycbyntG4TqopRKZnhrHvTwkDvIMR7tk1hxOMBfyXtu41u4sLjAU5FxxIO9x83aMYUMVypHg/exec"

def send_to_google_sheets(payload: dict):
    """
    Sends data to the Google Apps Script Webhook.
    This will be run as a background task.
    """
    if not WEBHOOK_URL:
        print("⚠️ Warning: No Google Sheets Webhook URL found in .env")
        return
        
    try:
        # Send the payload to Google
        response = requests.post(WEBHOOK_URL, json=payload, allow_redirects=True, timeout=15)
        print(f"✅ Synced to Sheets: {payload.get('team')} on {payload.get('date')}")
    except Exception as e:
        print(f"❌ Google Sheets Sync Error: {e}")