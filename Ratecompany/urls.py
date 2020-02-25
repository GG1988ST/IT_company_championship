from django.urls import path
from Ratecompany import views

app_name = 'Ratecompany'
urlpatterns = [
    path('Company/<slug:company_name_slug>/', views.show_company, name='show_company'),
]
