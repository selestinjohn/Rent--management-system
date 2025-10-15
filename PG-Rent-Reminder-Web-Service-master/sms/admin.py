from django.contrib import admin
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    # Show these fields in the admin list view (table)
    list_display = ('name', 'phone_number', 'message', 'due_date')

    # Add filters on the right sidebar
    list_filter = ('due_date',)

    # Enable search box in admin (by name, phone, or message)
    search_fields = ('name', 'phone_number', 'message')
