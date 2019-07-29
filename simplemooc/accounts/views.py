from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .form import RegisterForm


# Decorador para verificar se está logado antes de executar a view
@login_required
def dashboard(request):
    """
    View após logado
    """
    return render(request, 'accounts/dashboard.html')


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
            user = form.save()

            # Logando o usuário automaticamente
            user = authenticate(
                username=user.username,
                password=form.cleaned_data['password1']
            )
            login(request, user)

            # Redireciona para tela inicial
            return redirect('core:home')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)
