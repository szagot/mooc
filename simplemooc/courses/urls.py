from django.urls import path

from . import views

# Definindo namespace
app_name = 'courses'

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug:course_slug>', views.details, name='details'),
    path('<slug:course_slug>/inscricao', views.enrollments, name='enrollments'),
    path('<slug:course_slug>/inscricao/cancelar', views.undo_enrollment, name='undo_enrollment'),
    path('<slug:course_slug>/anuncios', views.announcements, name='announcements'),
    path('<slug:course_slug>/anuncios/<int:announcement_id>', views.show_announcement, name='announcement'),
    path('<slug:course_slug>/aulas', views.lessons, name='lessons'),
    path('<slug:course_slug>/aulas/<int:lesson_id>', views.show_lesson, name='show_lesson'),
]
