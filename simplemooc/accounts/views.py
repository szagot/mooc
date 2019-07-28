from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings


def register(request):
    """
    View para cadastro de novo usuário
    """
    # Verificando postagem
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # Formulário válido?
        if form.is_valid():
            # Salva os dados do form
            form.save()
            # Redireciona para a URL de login
            return redirect(settings.LOGIN_URL)
    else:
        form = UserCreationForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
