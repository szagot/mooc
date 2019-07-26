from django.urls import path

from . import views

# Definindo namespace
app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
]
