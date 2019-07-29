from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .form import RegisterForm


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
