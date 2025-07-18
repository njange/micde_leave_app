from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('apply/', views.apply_leave_view, name='apply_leave'),
    path('review/<int:application_id>/', views.review_leave_view, name='review_leave'),
    path('pdf/<int:application_id>/', views.view_pdf, name='view_pdf'),
]
