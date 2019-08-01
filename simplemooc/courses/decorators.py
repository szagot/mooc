from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Course, Enrollment


def enrollment_required(view_func):
    """
    Decorador para pegar o curso de uma inscrição
    """

    def get_course(request, *args, **kwargs):
        message = ''
        slug = kwargs.get('course_slug')
        # Pega o curso
        course = get_object_or_404(Course, slug=slug)
        # Tem permissão administrativa?
        has_permission = request.user.is_staff
        # Se não tem permissão administrativa, primeiro verifica se está inscrito ao curso
        if not has_permission:
            try:
                # Tenta pegar a inscrição
                enrollment = Enrollment.objects.get(user=request.user, course=course)

            # Inscrição inexistente
            except Enrollment.DoesNotExist:
                message = 'Desculpe, mas você não se inscreveu nesse curso.'

            else:
                # Está aprovado ao curso?
                if enrollment.is_approved():
                    has_permission = True
                else:
                    message = 'A sua inscrição ainda está pendente'

        # Se não tem permissão
        if not has_permission:
            messages.error(request, message)
            return redirect('accounts:dashboard')

        # grava o curso no request e retorna a função decorada
        request.course = course
        return view_func(request, *args, **kwargs)

    return get_course
