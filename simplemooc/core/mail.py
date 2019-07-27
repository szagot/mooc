from django.template.loader import render_to_string
from django.template.defaultfilters import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings


def send_mail_template(
        subject,
        template_name,
        context,
        recipient_list,
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=False
):
    """
    Centraliza aqui o envio de email usando templates
    """

    # Renderiza o tema
    message_html = render_to_string(template_name, context)
    # Converte para um formato de texto
    message_txt = strip_tags(message_html)
    # Configura o email primeiro como texto
    email = EmailMultiAlternatives(
        subject=subject,
        body=message_txt,
        from_email=from_email,
        to=recipient_list
    )
    # Configura o email como HTML
    email.attach_alternative(message_html, 'text/html')
    # Envia o email
    email.send(fail_silently=fail_silently)
