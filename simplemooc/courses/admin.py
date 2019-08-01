from django.contrib import admin

from .models import Course, Enrollment, Announcement, Comment, Lesson, Material


class CourseAdmin(admin.ModelAdmin):
    """
    Personaliza a amostragem do Model no Admin
    """
    # Campos a serem mostrados na listagem
    list_display = ['name', 'slug', 'start_date', 'created_at']
    # Campos em que o Admin fará a busca no campo de busca
    search_fields = ['name', 'slug']
    # Campos vinculados a outros. Exemplo: o Slug deve ser preenchido automaticamente baseado no nome
    prepopulated_fields = {'slug': ['name']}


class MaterialInlineAdmin(admin.StackedInline):
    """
    Para poder embutir o cadastro de materiais dentro de Aulas
    Outro formato é o admin.TabularInline, que coloca os campos lado a lado
    """
    model = Material


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    # Filtro lateral
    list_filter = ['created_at']
    # Embutindo o cadastro de materiais dentro de aulas
    inlines = [MaterialInlineAdmin]


admin.site.register(Course, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])
admin.site.register(Lesson, LessonAdmin)
