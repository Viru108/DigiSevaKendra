from django.urls import path
from . import views

urlpatterns = [
    path('head/', views.head_dashboard, name='head_dashboard'),
]
