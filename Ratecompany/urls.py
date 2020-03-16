from django.urls import path
from Ratecompany import views

app_name = 'Ratecompany'
urlpatterns = [
    path('',views.index,name='index'),
    path('Company/', views.show_category, name='show_category'),
]
