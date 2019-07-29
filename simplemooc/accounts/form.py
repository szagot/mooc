from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    """
    Personalizando o formulário padrão (UserCreationForm) para cadastro de usuário
    """
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        """
        Toda função clean_<campo>() é executada automaticamente para fazer verificações antes de salvar
        """
        email = self.cleaned_data['email']
        # Verifica se o email já existe em outro usuário
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe um usuário com esse email')

        # Se não existe duplicações, retorna o email
        return email

    def save(self, commit=True):
        """
        Substituindo o save() padrão para poder incluir o email
        """
        # Chamando o método save() original, porém sem salvar o usuário (commit=False)
        user = super().save(commit=False)
        # Adicionando campo de email
        user.email = self.cleaned_data['email']
        # Salvando, se quem chamou deixou no padrão
        if commit:
            user.save()

        return user


class EditAccountForm(forms.ModelForm):
    """
    Formulário de Edição de usuário
    """

    def clean_email(self):
        """
        Toda função clean_<campo>() é executada automaticamente para fazer verificações antes de salvar
        """
        email = self.cleaned_data['email']
        # Verifica se o email já existe, excluindo o usuário da própria instancia
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Outro usuário já está usando esse email')

        # Se não existe duplicações, retorna o email
        return email

    class Meta:
        # Define qual o modelo a ser usado
        model = User
        # Quais campos podem ser alterados?
        fields = ['username', 'email', 'first_name', 'last_name']