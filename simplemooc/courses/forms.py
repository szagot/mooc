from django import forms


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
