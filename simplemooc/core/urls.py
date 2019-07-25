from django.urls import path

from . import views

# Definindo namespace
app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('contato/', views.contact, name='contact'),
]