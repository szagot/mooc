from django.shortcuts import render, redirect
from .form import RegisterForm
from django.conf import settings


def register(request):
    """
    View para cadastro de novo usuário
    """
    # Verificando postagem
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        # Formulário válido?
        if form.is_valid():
            # Salva os dados do form
            form.save()
            # Redireciona para a URL de login
            return redirect(settings.LOGIN_URL)
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
