from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """
    Personalizando o formulário padrão (UserCreationForm) para cadastro de usuário
    """
    email = forms.EmailField(label='E-mail')

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
