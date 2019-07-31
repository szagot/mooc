import re

from django.db import models
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.conf import settings


class User(AbstractBaseUser, PermissionsMixin):
    # ## Campos customizados
    # Nome de usuário. Precisa ser único. Este campo tem validação de valores. Só são válidos os chars indicados
    username = models.CharField(
        'Nome de Usuário',
        max_length=30,
        unique=True,
        validators=[validators.RegexValidator(
            re.compile(r'^[\w.@+_-]+$'),
            'O nome de usuário só pode conter letras, números ou @.+_-',
            'invalid'
        )]
    )
    # O email é um campo único
    email = models.EmailField('E-mail', unique=True)
    # Não obrigatório
    name = models.CharField('Nome', max_length=100, blank=True)

    # ## Campos necessários para o funcionamento de User
    # Não é obrigatório, mas terá como valor padrão True
    is_active = models.BooleanField('Está Ativo?', blank=True, default=True)
    # Se é da área administrativa
    is_staff = models.BooleanField('É Admin?', blank=True, default=False)
    # Campo atualizado automaticamente no INSERT
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)

    # Manager do User
    objects = UserManager()

    # Campo único e referencia na hora do login
    USERNAME_FIELD = 'username'
    # Campos obrigatórios para superusuário
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.name or self.username

    def get_short_name(self):
        """
        Descrição curta do nome
        """
        return self.username

    def get_full_name(self):
        """
        Descrição completa do nome. Retorna a representação string deste objeto
        """
        return str(self)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class PasswordReset(models.Model):
    """
    Classe para gerar uma nova senha aleatória quando o usuário esqueceu a senha
    """
    # Chave estrangeira. O pai é o User.id (ou User.pk). Normalmente, basta informar o model. Mas aqui,
    # por se tratar de uma herança do Django, há a necessidade de usar a chave criada em settings
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        on_delete=models.CASCADE,
        # Serve pra indicar qual o nome do objeto para se trazer todos os PasswordsResets do usuário.
        # Se não for indicado, o objeto será sempre '<nomedomodel>_set'
        # Exemplo: resets = user.resets.all()
        related_name='resets'
    )
    key = models.CharField('Chave', max_length=100, unique=True)
    confirmed = models.BooleanField('Confirmado?', default=False, blank=True)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return f'{self.user} em {self.created_at}'

    class Meta:
        verbose_name = 'Nova Senha'
        verbose_name_plural = 'Novas Senhas'
        # Ordenando de modo decrescente pela data
        ordering = ['-created_at']
