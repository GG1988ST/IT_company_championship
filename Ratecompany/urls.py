from django.urls import path
from Ratecompany import views

app_name = 'Ratecompany'
urlpatterns = [
    path('Company/', views.show_company, name='show_company'),
]
