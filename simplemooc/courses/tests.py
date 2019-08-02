from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse
from django.conf import settings

from .models import Course


class ContactCourseTestCase(TestCase):
    """
    Testa o formulário de contato do curso
    """

    @classmethod
    def setUpClass(cls):
        """
        Executado antes de todos os teses
        """
        pass

    def setUp(self):
        """
        Executado antes de CADA teste
        """
        # Cria um registro no BD
        self.course = Course.objects.create(name='Django', slug='django')

    def tearDown(self):
        """
        Executado depois de CADA teste
        """
        # Apaga o registro de teste criado
        self.course.delete()

    @classmethod
    def tearDownClass(cls):
        """
        Executado depois de todos os testes
        """
        pass

    def test_contact_form_error(self):
        """
        Teste os avisos de erro no formulário de contato
        """
        data = {'name': 'Fulano de Tal', 'email': '', 'message': ''}
        client = Client()
        path = reverse('courses:details', args=[str(self.course.slug)])
        response = client.post(path, data)
        # Testa se deu erro no campo email
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        # Testa se deu erro no campo mensagem
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')

    def test_contact_form_success(self):
        """
        Testa se houve sucesso no envio de dados
        """
        data = {'name': 'Fulano de Tal', 'email': 'szagot@gmail.com', 'message': 'Teste'}
        client = Client()
        path = reverse('courses:details', args=[str(self.course.slug)])
        client.post(path, data)
        # Testa se foi tem 1 email na caixa de saída de emails
        self.assertEqual(len(mail.outbox), 1)
        # Testa se o email foi enviado para a pessoa certa
        self.assertEqual(mail.outbox[0].to[0], settings.CONTACT_EMAIL)
