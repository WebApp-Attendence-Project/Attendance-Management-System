from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='aboutUs'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('attendence/', views.attendence, name='attendence'),
    path('login', views.handleLogin, name="handleLogin"),
    path('logout', views.handleLogout, name="handleLogout"),
    path('save_data/', views.save_data, name="save_data"),
    path('attendence_report/', views.attendence_report, name="attendence_report"),
    path('admin_get_attendence/', views.admin_get_attendence, name="admin_get_attendence"),
    path('get_attendence/', views.get_attendence, name="get_attendence"),
    path('staff_details/', views.staff_details, name="staff_details"),
    path('all_staff/', views.all_staff, name="all_staff"),
    path('from_to_staff_attendance/', views.from_to_staff_attendance, name="from_to_staff_attendance"),
    path('export_excel/', views.export_excel, name="export_excel"),

]
