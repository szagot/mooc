from django.db import models
from django.conf import settings


class CourseManager(models.Manager):
    """
    Gerenciador da tabela do BD
    Substitui o objects padrão do Django
    """

    def search(self, query):
        """
        Pesquisa dentro da tabela, pelo conteúdo do nome ou pelo conteudo da descrição
        """
        return self.get_queryset().filter(
            # Usando o models.Q é possível definir o tipo de pesquisa entre os campos
            # | = OR
            # & = AND
            # [campo]__icontains = query
            models.Q(name__icontains=query) | models.Q(description__icontains=query)
        )


class Course(models.Model):
    """
    Modelo para Tabela do BD
    """
    # Campo de texto
    name = models.CharField(
        'Nome',
        max_length=100
    )

    # Campo de Texto para slugs
    slug = models.SlugField(
        'Atalho'
    )

    # Campo de textos longos. blank informa que o campo não é obrigatório
    description = models.TextField(
        'Descrição Simples',
        blank=True
    )

    about = models.TextField(
        'Sobre o Curso',
        blank=True
    )

    # Campo de Data. Não é obrigatório e pode ser NULL no BD
    start_date = models.DateField(
        'Data de Início',
        null=True,
        blank=True
    )

    # Campo de imagem. Irá salvar no diretório indicado, porém dentro de MEDIA_ROOT indicado em settings.py
    # Campo dependente da biblioteca Pillow que não vem instalada no Python por padrão
    image = models.ImageField(
        'Imagem',
        upload_to='courses/images',
        null=True,
        blank=True
    )

    # Data/Hora que será preenchido automaticamente no INSERT
    created_at = models.DateTimeField(
        'Criado em',
        auto_now_add=True
    )

    # Data/Hora que será preenchido automaticamente no UPDATE
    updated_at = models.DateTimeField(
        'Atualizado em',
        auto_now=True
    )

    # Substitui o object padrão (manager padrão) pelo acima
    objects = CourseManager()

    def __str__(self):
        """
        Importante para o Admin imprimir automaticamente o nome correto para o objeto
        """
        return self.name

    def get_absolute_url(self):
        """
        Necessário para retornar a url absoluta com o link correto (cursos/<slug>)
        No template use: {{ course.get_absolute_url }} ou {% url 'courses:details' course.slug %}
        Se usar a segunda forma, esse método não é mais necessario, mas no admin não vai aparecer a opção 'ver no site'
        """
        from django.urls import reverse
        return reverse('courses:details', args=[str(self.slug)])

    class Meta:
        """
        Importante para a tradução do nome da Classe
        """
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        # Para definir em ordem decrescente, coloque o sinal - na frente. Ex.: ['-name']
        ordering = ['name']


class Enrollment(models.Model):
    """
    Modelo para Inscrições de Curso
    """

    # Escolhas para Status
    STATUS_CHOICES = (
        (0, 'Pendente'),
        (1, 'Aprovado'),
        (2, 'Cancelado'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='enrollments',
        on_delete=models.CASCADE
    )

    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='enrollments',
        on_delete=models.CASCADE
    )

    status = models.IntegerField(
        'Situação',
        choices=STATUS_CHOICES,
        default=0,
        blank=True
    )

    created_at = models.DateTimeField(
        'Criado Em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado Em',
        auto_now=True
    )

    def active(self):
        """
        Ativando curso do aluno
        """
        self.status = 1
        self.save()

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # Garante que não haverá repetição de cursos para o mesmo usuário (liter. Juntos somos Únicos).
        # Cada tupla interna da tupla principal indica as uniões de campos que não devem se repetir
        unique_together = (('user', 'course'),)
