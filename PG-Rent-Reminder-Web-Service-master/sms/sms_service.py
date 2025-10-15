# sms/sms_service.py
from django.conf import settings
import requests
from requests.auth import HTTPBasicAuth


def send_sms(to, body):
    """
    Send an SMS via Beem Africa
    - to: recipient phone number (string, e.g. +2557xxxxxxx)
    - body: message text (string)
    """
    api_key = getattr(settings, "BEEM_API_KEY", None)
    secret_key = getattr(settings, "BEEM_SECRET_KEY", None)

    if not api_key or not secret_key:
        raise ValueError("Beem API credentials not configured in settings.py")

    url = "https://apisms.beem.africa/v1/send"
    data = {
        "source_addr": "SELTECH",  # must exactly match your approved Sender ID
        "encoding": 0,
        "message": body,
        "recipients": [{"recipient_id": 1, "dest_addr": to.lstrip("+")}]
    }

    response = requests.post(url, json=data, auth=HTTPBasicAuth(api_key, secret_key))

    if response.status_code == 200:
        print(f"✅ SMS sent to {to}")
        print("Response:", response.text)
    else:
        print(f"❌ Failed to send SMS to {to}")
        print("Response:", response.text)
