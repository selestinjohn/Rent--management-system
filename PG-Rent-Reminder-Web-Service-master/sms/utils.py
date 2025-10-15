# sms/utils.py
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings


def send_sms(phone_number: str, message: str):
    """
    Send SMS using Beem Africa API
    """
    # ✅ Ensure credentials exist in settings.py
    api_key = getattr(settings, "BEEM_API_KEY", None)
    secret_key = getattr(settings, "BEEM_SECRET_KEY", None)

    if not api_key or not secret_key:
        raise ValueError("Beem API credentials not configured in settings.py")

    url = "https://apisms.beem.africa/v1/send"

    payload = {
        "source_addr": "INFO",   # Can be customized in Beem dashboard
        "encoding": 0,
        "message": message,
        "recipients": [
            {
                "recipient_id": 1,
                "dest_addr": phone_number  # Must be without + (e.g. 2557...)
            }
        ]
    }

    try:
        response = requests.post(
            url,
            json=payload,
            auth=HTTPBasicAuth(api_key, secret_key)
        )

        if response.status_code == 200:
            return {"success": True, "response": response.json()}
        else:
            return {
                "success": False,
                "status_code": response.status_code,
                "response": response.text,
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
