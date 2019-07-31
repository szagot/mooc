from django import forms
from django.contrib.auth import get_user_model

# Isso se faz necessário porque o User é customizado. Isso fará o Django pegar o model criado
User = get_user_model()


class RegisterForm(forms.ModelForm):
    """
    Personalizando o formulário padrão (UserCreationForm) para cadastro de usuário
    """

    # Campos para senha
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmação de Senha', widget=forms.PasswordInput)

    def clean_password2(self):
        """
        Toda função clean_<campo>() é executada automaticamente para fazer verificações antes de salvar
        Neste caso, compara se o a senha de confirmação é a mesma que a senha
        """
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password1']
        # Se a senha foi informada mas os campos não coincidem
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Os campos de senha e confirmação não são iguais', code='password_mismatch')

        return password2

    # Não é mais necessário porque agora o User é customizado e já obriga o email único
    # def clean_email(self):
    #     """
    #     Toda função clean_<campo>() é executada automaticamente para fazer verificações antes de salvar
    #     """
    #     email = self.cleaned_data['email']
    #     # Verifica se o email já existe em outro usuário
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Já existe um usuário com esse email')
    #
    #     # Se não existe duplicações, retorna o email
    #     return email

    def save(self, commit=True):
        """
        Substituindo o save() padrão para poder incluir o email
        """
        # Chamando o método save() original, porém sem salvar o usuário (commit=False)
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # Salvando, se quem chamou deixou no padrão
        if commit:
            user.save()

        return user

    class Meta:
        model = User
        fields = ['username', 'email']


class PasswordResetForm(forms.Form):
    """
    Formulário para reset de senha.
    """
    email = forms.EmailField(label='E-mail')

    def clean_email(self):
        email = self.cleaned_data['email']
        # Verifica se tem um usuário com esse email
        if User.objects.filter(email=email).exists():
            return email

        raise forms.ValidationError('Nenhum usuário encontrado com este email')


class EditAccountForm(forms.ModelForm):
    """
    Formulário de Edição de usuário
    """

    # Não é mais necessário porque agora o User é customizado e já obriga o email único
    # def clean_email(self):
    #     """
    #     Toda função clean_<campo>() é executada automaticamente para fazer verificações antes de salvar
    #     """
    #     email = self.cleaned_data['email']
    #     # Verifica se o email já existe, excluindo o usuário da própria instancia
    #     if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
    #         raise forms.ValidationError('Outro usuário já está usando esse email')
    #
    #     # Se não existe duplicações, retorna o email
    #     return email

    class Meta:
        # Define qual o modelo a ser usado
        model = User
        # Quais campos podem ser alterados?
        fields = ['username', 'email', 'name']
