from django.urls import path
from sms import views

urlpatterns = [
    path('', views.index, name='home'),
    path('ser/', views.service, name='service'),
    #path('sms/', views.sms, name='sms'),#
    #path('all/', views.all_alert, name='all'),
    path('add-tenant/', views.add_tenant, name='add_tenant'),  # updated
]
