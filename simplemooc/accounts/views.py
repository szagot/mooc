from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from .form import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset
from ..core.utils import generate_hash_key

# Isso se faz necessário porque o User é customizado. Isso fará o Django pegar o model criado
User = get_user_model()


def register(request):
    """
    View para cadastro de novo usuário
    """
    # Verificando postagem
    form = RegisterForm(request.POST or None)
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

    return render(request, 'accounts/register.html', {'form': form})


def password_reset(request):
    """
    View para gerar nova senha, quando o usuário a esqueceu
    """
    context = {}

    # Se houve POST, informa, senão cria um form vazio
    form = PasswordResetForm(request.POST or None)
    # Teve postagem, e o fomulário está valido?
    if form.is_valid():
        # Gera uma nova senha
        user = User.objects.get(email=form.cleaned_data['email'])
        key = generate_hash_key(user.username)
        reset = PasswordReset(key=key, user=user)
        reset.save()
        context['success'] = True

    context['form'] = form

    return render(request, 'accounts/password_reset.html', context)


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
    form = EditAccountForm(request.POST or None, instance=request.user)
    if form.is_valid():
        # Salva o formulário e marca como OK
        form.save()
        form = EditAccountForm(instance=request.user)
        context['success'] = True

    context['form'] = form
    return render(request, 'accounts/dashboard/edit.html', context)


@login_required
def edit_password(request):
    """
    Alteração de senha
    """
    context = {}

    # Teve postagem?
    form = PasswordChangeForm(data=request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        form = PasswordChangeForm(user=request.user)
        context['success'] = True

    context['form'] = form
    return render(request, 'accounts/dashboard/edit-pass.html', context)
