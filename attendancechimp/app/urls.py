from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('success/', views.success, name='success'),
    path('course_success/', views.course_success, name='course_success'),
    path('join/<int:course_id>/', views.join, name='join'),
    path('attendance/', views.attendance, name='attendance'),
    path('upload/', views.upload, name='upload'),
]
