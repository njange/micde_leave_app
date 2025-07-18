from django.urls import path
from django.shortcuts import redirect
from . import views

def redirect_to_dashboard(request):
    """Redirect root URL to dashboard if authenticated, otherwise to login."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

urlpatterns = [
    path('', redirect_to_dashboard, name='home'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('apply/', views.apply_leave_view, name='apply_leave'),
    path('review/<int:application_id>/', views.review_leave_view, name='review_leave'),
    path('pdf/<int:application_id>/', views.view_pdf, name='view_pdf'),
]
