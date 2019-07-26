from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    """
    Personaliza a amostragem do Model no Admin
    """
    # Campos a serem mostrados na listagem
    list_display = ['name', 'slug', 'start_date', 'created_at']
    # Campos em que o Admin fará a busca no campo de busca
    search_fields = ['name', 'slug']
    # Campos "linkados" a outros. Exemplo: o Slug deve ser preenchido automaticamente baseado no nome
    prepopulated_fields = {'slug': ['name']}


admin.site.register(Course, CourseAdmin)
