from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Course, Enrollment
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

    # Houve postagem e Formulário é válido?
    form = ContactCourse(request.POST or None)
    if form.is_valid():
        # Adiciona uma tag ao contexto
        contexto['is_valid'] = True
        # Se precisar acessar os dados validados do formulário, eles estarão no dicionário:
        # form.cleaned_data

        # Envia email e limpa o formulário por estar válido
        form.send_mail(curso)
        form = ContactCourse()

    contexto['form'] = form
    contexto['course'] = curso

    return render(request, 'courses/detalhe.html', contexto)


@login_required
def enrollments(request, course_slug):
    """
    View para inscrições
    :param request:
    :param course_slug: slug do curso a ser adicionado
    """
    course = get_object_or_404(Course, slug=course_slug)
    # Pega uma associação ou cria automaticamente para usuário/curso. O segundo parametro é se criou ou não (bool)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    # Precisou criar?
    if created:
        enrollment.active()
        messages.success(request, 'Você foi inscrito no curso com sucesso :)')
    else:
        messages.info(request, 'Você já está inscrito neste curso ;)')

    return redirect('accounts:dashboard')


@login_required
def undo_enrollment(request, course_slug):
    # Pegando curso
    course = get_object_or_404(Course, slug=course_slug)
    # Pegando inscrição
    enrollment = get_object_or_404(Enrollment, course=course, user=request.user)

    # Confirmou remoção da inscrição?
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Sua inscrição foi cancelada com sucesso!')
        return redirect('accounts:dashboard')

    return render(request, 'courses/dashboard/undo_enrollment.html', {
        'course': course
    })


@login_required
def announcements(request, course_slug):
    """
    View para anuncios do curso no dashboard
    """
    # Pegando curso
    course = get_object_or_404(Course, slug=course_slug)
    # Verifica a inscrição apenas se não for um membro administrador
    if not request.user.is_staff:
        # Pegando inscrição
        enrollment = get_object_or_404(Enrollment, course=course, user=request.user)
        # Verifica se o aluno está aprovado no curso
        if not enrollment.is_approved():
            messages.error(request, 'A sua inscrição está pendente')
            return redirect('accounts:dashboard')

    return render(request, 'courses/dashboard/announcements.html', {
        'course': course,
        'announcements': course.announcements.all()
    })
