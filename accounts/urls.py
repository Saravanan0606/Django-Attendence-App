from django.urls import path

from accounts import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('record_attendance/', views.record_attendance, name='record_attendance'),
    path('attendence/', views.attendence, name='attendence'),
    path('attendence/view_attendance/', views.view_attendance, name='view_attendance'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout, name='logout'),
]