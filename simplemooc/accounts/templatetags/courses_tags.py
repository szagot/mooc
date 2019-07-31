"""
Criando TAGs de Templates para Cursos
"""
from django import template
from simplemooc.courses.models import Enrollment

register = template.Library()


@register.simple_tag
def my_courses(user):
    """
    Pegando todos os cursos inscritos do usuário informado
    """
    return Enrollment.objects.filter(user=user)
