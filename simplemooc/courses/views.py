from django.shortcuts import render
from .models import Course


def index(request):
    # Pegando todos os cursos
    cursos = Course.objects.all()
    return render(request, 'courses/index.html', {
        'courses': cursos
    })


def details(request, course_id):
    curso = Course.objects.get(pk=course_id)
    return render(request, 'courses/detalhe.html', {
        'course': curso
    })
