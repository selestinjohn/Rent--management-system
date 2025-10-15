from django.db import models  # ✅ Import models

class Contact(models.Model):
    name = models.CharField(max_length=100)           # Tenant name
    phone_number = models.CharField(max_length=100)   # Tenant phone
    message = models.CharField(max_length=255)        # Reminder message
    due_date = models.DateField()
    sms_sent =models.BooleanField(default=False) #new field                    # Rent due date

    def __str__(self):
        # This string shows up in dropdowns/relations in admin
        return f"{self.name} - {self.phone_number} - {self.due_date}"
