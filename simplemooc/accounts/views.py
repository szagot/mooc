from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .form import RegisterForm, EditAccountForm


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


# Decorador para verificar se está logado antes de executar a view
@login_required
def dashboard(request):
    """
    View após logado
    """
    return render(request, 'accounts/dashboard.html')


@login_required
def edit(request):
    """
    Editando usuário
    """
    context = {}

    # Houve postagem?
    if request.method == 'POST':
        # Pega a postagem e verifica se os dados estão válidos
        form = EditAccountForm(request.POST, instance=request.user)
        if form.is_valid():
            # Salva o formulário e marca como OK
            form.save()
            form = EditAccountForm(instance=request.user)
            context['success'] = True
    else:
        form = EditAccountForm(instance=request.user)

    context['form'] = form
    return render(request, 'accounts/dashboard/edit.html', context)


@login_required
def edit_password(request):
    """
    Alteração de senha
    """
    context = {}

    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            form = PasswordChangeForm(user=request.user)
            context['success'] = True
    else:
        form = PasswordChangeForm(user=request.user)

    context['form'] = form
    return render(request, 'accounts/dashboard/edit-pass.html', context)
