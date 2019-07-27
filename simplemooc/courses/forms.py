from django import forms
from django.core.mail import send_mail
from django.conf import settings


class ContactCourse(forms.Form):
    """
    Classe para Formulário de Contato

    Sempre use dentro da tag <form>:
        {% csrf_token %}

    Para renderizar, no template use:
        {{ form }}              apenas os campos
        {{ form.as_p }}         campos dentro de paragrafos
        {{ form.as_table }}     campos dentro de uma tabela (Ele não adiciona a tag <table>)
    Para campos personalizados, faça:
        {% for field in form }%
            {{ field.label_tag }} (ou {{ field.label }} se quiser apenas o texto do label)
            {{ field }}
            # Imprima apenas {{ field.errors }} ou, se quiser personalizar faça:
            {% if field.errors %}
                {% for error in field.errors %}
                    <p>{{ error }}</p>
                {% endfor %}
            {% endif %}
        {% endfor %}
    """
    # Campo Nome
    name = forms.CharField(label='Nome', max_length=100, required=False)
    # Campo Email
    email = forms.EmailField(label='E-mail')
    # Campo Mensagem. Não existe o tipo TextField. Ao invés, use o widget
    message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

    def send_mail(self, course):
        """
        Definindo envio de email
        """
        subject = f'[{course}] | Contato'
        message = f'Nome: {self.cleaned_data["name"]};' + \
                  f'E-mail: {self.cleaned_data["email"]};' + \
                  f'{self.cleaned_data["message"]}'
        send_mail(
            subject,
            message,
            # De
            settings.DEFAULT_FROM_EMAIL,
            # Para
            [settings.CONTACT_EMAIL]
        )
