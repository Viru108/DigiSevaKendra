from django.urls import path
from . import views, status_views

urlpatterns = [
    path('raise/', views.raise_complaint, name='raise_complaint'),
    path('api/categories/', views.get_categories, name='get_categories'),
    path('status/update/<str:ticket_id>/', status_views.update_complaint_status, name='update_complaint_status'),
    path('resolve/<str:ticket_id>/', views.resolve_complaint, name='resolve_complaint_tech'),
]

