from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

# Definindo namespace
app_name = 'accounts'

urlpatterns = [
    # Usando a view do próprio Django para Login de usuários (não tem a ver com o ADMIN)
    path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Usando a view do próprio Django para Logout
    path('sair/', LogoutView.as_view(next_page='core:home'), name='logout'),

    path('cadastro/', views.register, name='register'),
]
