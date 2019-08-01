from django.db import models
from django.conf import settings
from ..core.mail import send_mail_template


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


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='lessons',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        'Nome',
        max_length=100
    )

    description = models.TextField(
        'Descrição',
        blank=True
    )

    # Ordenação dos cursos
    number = models.IntegerField(
        'Número (ordem)',
        blank=True,
        default=0
    )

    # Data de liberação
    release_date = models.DateField(
        'Data de Liberação',
        blank=True,
        null=True
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Aula'
        verbose_name_plural = 'Aulas'
        ordering = ['number']


class Material(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        verbose_name='Aula',
        related_name='materials',
        on_delete=models.CASCADE
    )

    name = models.CharField(
        'Nome',
        max_length=100
    )

    embedded = models.TextField(
        'Vídeos e Conteúdo Embutido',
        blank=True,
        null=True
    )

    file = models.FileField(
        upload_to='lessons/materials',
        blank=True,
        null=True
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

    def is_embedded(self):
        """
        É do tipo embutido? Ou arquivo?
        :return: True para embutido, False para arquivo
        """
        return bool(self.embedded)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Material'
        verbose_name_plural = 'Materiais'


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

    def is_approved(self):
        """
        Verifica se o usuário está aprovado para o curso
        """
        return self.status == 1

    class Meta:
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'
        # Garante que não haverá repetição de cursos para o mesmo usuário (liter. Juntos somos Únicos).
        # Cada tupla interna da tupla principal indica as uniões de campos que não devem se repetir
        unique_together = (('user', 'course'),)


class Announcement(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name='Curso',
        related_name='announcements',
        on_delete=models.CASCADE
    )

    title = models.CharField(
        'Título',
        max_length=100
    )

    content = models.TextField(
        'Conteúdo'
    )

    created_at = models.DateTimeField(
        'Criado Em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado Em',
        auto_now=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Anúncio'
        verbose_name_plural = 'Anúncios'
        ordering = ['-created_at']


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement,
        verbose_name='Anúncio',
        related_name='comments',
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='Usuário',
        related_name='users',
        on_delete=models.CASCADE
    )

    comment = models.TextField(
        'Comentário'
    )

    created_at = models.DateTimeField(
        'Criado Em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        'Atualizado Em',
        auto_now=True
    )

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['created_at']


def post_save_announcement(instance: Announcement, created, **kwargs):
    """
    Signal. Gatilho a ser disparado após salvar um anúncio.
    Será enviado um email aos inscritos do curso relacionado ao anúncio

    :param instance: A instancia deste sinal que deve ser sempre o model Announcement
    :param created: A ação foi disparada na criação? Se for no update, o valor seá False
    :param kwargs: Demais parâmetros do disparo. Obrigatório informar
    """
    # Envia apenas ser for na criação
    if created:
        context = {
            'announcement': instance
        }
        # Pegando inscrições relacionados ao anuncio
        enrollments = Enrollment.objects.filter(course=instance.course, status=1)
        # Enviando email para cada inscrito separadamente
        for enrollment in enrollments:
            send_mail_template(instance.title, 'courses/announcements_mail.html', context, [enrollment.user.email])


# Registrando Gatilho de Pós Salvamento
models.signals.post_save.connect(
    # Função a ser executada
    post_save_announcement,
    # Qual o modelo que deve disparar o sinal
    sender=Announcement,
    # Evita que o sinal seja cadastrado em duplicidade
    dispatch_uid='post_save_announcement'
)
