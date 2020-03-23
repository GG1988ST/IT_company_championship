from django.urls import path
from Ratecompany.views import *

app_name = 'Ratecompany'
urlpatterns = [
    path('Company/', CompanyListView.as_view(), name='company_list'),
    path('Company/<int:id>/', CompanyDetailView.as_view(), name='company_detail'),
    path('comment-list/', CommentListView.as_view(), name='comment-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('rate/', RateView.as_view(), name='rate'),
]
