# notifications.py
from twilio.rest import Client
from django.conf import settings
from datetime import datetime

# Initialize Twilio client using credentials from settings
client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_sms(to, body):
    """
    Send an SMS via Twilio.
    Returns the message SID on success, None on failure.
    """
    try:
        message = client.messages.create(
            body=body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
        print(f"✅ SMS sent to {to} (SID: {message.sid})")
        return message.sid
    except Exception as e:
        print(f"❌ Failed to send SMS to {to}: {e}")
        return None

def notify_tenant(tenant, days_before=5):
    """
    Check if the tenant's due date is within the 'days_before' threshold.
    If yes, send a personalized SMS notification.
    """
    today = datetime.now().date()
    days_until_due = (tenant.due_date - today).days

    # Only send SMS if due date is within the threshold
    if 0 <= days_until_due <= days_before:
        try:
            # Format the message using tenant info
            sms_text = tenant.message.format(
                name=tenant.name,
                due_date=tenant.due_date
            )
            return send_sms(tenant.phone_number, sms_text)
        except Exception as e:
            print(f"❌ Error preparing or sending SMS for tenant {tenant.name}: {e}")
            return None
    else:
        print(f"ℹ️ No SMS sent for {tenant.name}. Due in {days_until_due} days.")
        return None
