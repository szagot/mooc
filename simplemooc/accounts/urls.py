from django.urls import path

from django.contrib.auth.views import LoginView

# Definindo namespace
app_name = 'accounts'

urlpatterns = [
    # Usando a view do próprio Django para Login de usuários (não tem a ver com o ADMIN)
    path('entrar/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]
