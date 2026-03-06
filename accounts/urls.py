from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('manage/add-officer/', views.add_officer_view, name='add_officer'),
    path('manage/add-technician/', views.add_technician_view, name='add_technician'),
    path('manage/remove-technician/<int:tech_id>/', views.remove_technician_view, name='remove_technician'),
]
