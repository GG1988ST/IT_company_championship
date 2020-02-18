from django.urls import path
from company import views

app_name = 'company'
urlpatterns = [
    path('<slug:company_name_slug>/', views.show_company, name='show_company'),
]