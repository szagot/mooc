from django.urls import path

from . import views

# Definindo namespace
app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>', views.details, name='details'),
]
