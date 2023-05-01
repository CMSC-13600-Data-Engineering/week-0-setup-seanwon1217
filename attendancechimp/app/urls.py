from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.new, name='new'),
    path('create/', views.create, name='create'),
    path('success/', views.success, name='success'),
    #path('course_successs/', views.course_successs, name='course_successs'),
    path('join/', views.join, name='join'),
    path('attendance/', views.attendance, name='attendance'),
    path('student_list/', views.student_list, name='student_list'),
    path('course_success/<int:course_id>/', views.course_success, name='course_success'),
    #path('course_success/', views.create, name='course_success'),
    path('upload/', views.upload, name='upload'),
    path('course_list/', views.course_list, name='course_list'),
    path('overview/', views.overview, name='overview'),
    path('student/', views.student, name='student'),
]
