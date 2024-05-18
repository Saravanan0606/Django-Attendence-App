from django.urls import path
from accounts import views

urlpatterns = [
    path('login/', views.login, name='login'),
    # path('record_attendance/', views.record_attendence, name='record_attendance'),  # Remove this if integrated into landing_page
    path('attendence/', views.attendence, name='attendence'),
    # path('view_attendence/', views.view_attendence, name='view_attendence'),  # Remove this if integrated into landing_page
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
    path('landing/', views.landing_page, name='landing_page'),  # Add this for the landing page view
]
