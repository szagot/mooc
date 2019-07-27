from django.shortcuts import render, get_object_or_404
from .models import Course
from .forms import ContactCourse


def index(request):
    # Pegando todos os cursos
    cursos = Course.objects.all()
    return render(request, 'courses/index.html', {
        'courses': cursos
    })


def details(request, course_slug):
    # Esse método funciona, mas pode retornar erro se o ID não existir.
    # curso = Course.objects.get(pk=course_id)  # ou slug=<variavel_slug>

    # O ideal é usar assim, para direcionar à pagina 404 se o objeto não existir:
    curso = get_object_or_404(Course, slug=course_slug)  # ou pk=<variavel_id>
    contexto = {}

    # Pegando postagem do form
    if request.method == 'POST':
        form = ContactCourse(request.POST)
        # Formulário é válido?
        if form.is_valid():
            # Adiciona uma tag ao contexto
            contexto['is_valid'] = True
            # Se precisar acessar os dados validados do formulário, eles estarão no dicionário:
            # form.cleaned_data

            # Limpa o formulário por estar válido
            form = ContactCourse()
    else:
        form = ContactCourse()

    contexto['form'] = form
    contexto['course'] = curso

    return render(request, 'courses/detalhe.html', contexto)
