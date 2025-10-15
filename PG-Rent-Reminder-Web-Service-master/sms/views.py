from django.shortcuts import render, HttpResponse
from .models import Contact
from .utils import send_sms

def index(request):
    return render(request, 'index.html')

def service(request):
    contacts = Contact.objects.all()
    return render(request, 'service.html', {'data': contacts})

def add_tenant(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("number")
        message_text = request.POST.get("message")
        due_date = request.POST.get("dates")

        if not name or not phone or not message_text or not due_date:
            return HttpResponse("<p style='color:red;'>❌ Missing required fields</p>")

        contact = Contact.objects.create(
            name=name,
            phone_number=phone,
            message=message_text,
            due_date=due_date
        )

        # Send SMS immediately if you want
        sms_text = message_text.format(name=name, due_date=due_date)
        send_sms(phone, sms_text)

        return HttpResponse(f"<p style='color:green;'>✅ Tenant {name} added & SMS sent!</p>")

    return HttpResponse("<p style='color:red;'>❌ Invalid request method</p>")
