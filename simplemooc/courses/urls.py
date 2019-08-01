from django.urls import path

from . import views

# Definindo namespace
app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:course_slug>', views.details, name='details'),
    path('<slug:course_slug>/inscricao', views.enrollments, name='enrollments'),
    path('<slug:course_slug>/anuncios', views.announcements, name='announcements'),
]
