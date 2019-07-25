from django.db import models


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
    name = models.CharField('Nome', max_length=100)
    # Campo de Texto para slugs
    slug = models.SlugField('Atalho')
    # Campo de textos longos. blank informa que o campo não é obrigatório
    description = models.TextField('Descrição', blank=True)
    # Campo de Data. Não é obrigatório e pode ser NULL no BD
    start_date = models.DateField('Data de Início', null=True, blank=True)
    # Campo de imagem. Irá salvar no diretório indicado, porém dentro de MEDIA_ROOT indicado em settings.py
    # Campo dependente da biblioteca Pillow que não vem instalada no Python por padrão
    image = models.ImageField('Imagem', upload_to='courses/images', null=True, blank=True)

    # Data/Hora que será preenchido automaticamente no INSERT
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    # Data/Hora que será preenchido automaticamente no UPDATE
    updated_at = models.DateTimeField('Atualizado em', auto_now=True)

    # Substitui o object padrão (manager padrão) pelo acima
    objects = CourseManager()
