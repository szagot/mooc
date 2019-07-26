from django.shortcuts import render, get_object_or_404
from .models import Course


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

    return render(request, 'courses/detalhe.html', {
        'course': curso
    })
