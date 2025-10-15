# sms/tasks.py
from celery import shared_task
from django.conf import settings
from datetime import date
import requests
from requests.auth import HTTPBasicAuth
from .models import Contact

def send_sms_beem(phone_number, message_text):
    """
    Send SMS via Beem Africa API
    """
    api_key = getattr(settings, "BEEM_API_KEY", None)
    secret_key = getattr(settings, "BEEM_SECRET_KEY", None)

    if not api_key or not secret_key:
        raise ValueError("Beem API credentials not configured in settings.py")

    url = "https://apisms.beem.africa/v1/send"
    data = {
        "source_addr": "SELTECH",  # Your sender ID
        "encoding": 0,
        "message": message_text,
        "recipients": [{"recipient_id": 1, "dest_addr": phone_number.lstrip("+")}]
    }

    response = requests.post(url, json=data, auth=HTTPBasicAuth(api_key, secret_key))

    if response.status_code == 200:
        print(f"✅ SMS sent to {phone_number}")
    else:
        print(f"❌ Failed to send SMS to {phone_number}")
        print("Response:", response.text)


@shared_task
def check_due_dates_and_send_sms():
    """
    Celery task to check today's due dates and send SMS
    """
    today = date.today()
    due_contacts = Contact.objects.filter(due_date=today, sms_sent=False)

    if not due_contacts:
        print("No due dates for today.")
        return None

    for contact in due_contacts:
        try:
            sent = send_sms_beem(contact.phone_number, contact.message)
            if sent:
                contact.sms_sent = True   # ✅ mark as sent
                contact.save(update_fields=['sms_sent'])
                print(f"✅ Marked {contact.phone_number} as sent.")
        except Exception as e:
            print(f"Error sending SMS to {contact.phone_number}: {e}")

    return None
