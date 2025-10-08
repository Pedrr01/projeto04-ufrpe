from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UserAuthTests(TestCase):
    def setUp(self):
        # Define URLs e dados de teste comuns
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.username = 'testuser'
        self.password = 'ComplexPass123!'
        self.login_data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
        }

    def test_signup_creates_user_and_redirects_to_login(self):
        """
        Testa o cadastro de usuário: verifica criação, redirecionamento e senha hasheada.
        """
        response = self.client.post(self.signup_url, self.login_data)

        self.assertRedirects(response, self.login_url)
        self.assertTrue(User.objects.filter(username=self.username).exists())
        user = User.objects.get(username=self.username)
        self.assertTrue(user.check_password(self.password))

    def test_signup_with_existing_username(self):
        """
        Testa cadastro com nome de usuário já existente: deve retornar erro.
        """
        User.objects.create_user(username=self.username, password=self.password)

        response = self.client.post(self.signup_url, self.login_data)

        self.assertEqual(response.status_code, 200)
        # Mensagem padrão do Django para formulário de usuário duplicado
        self.assertContains(response,  "nome de usuário já existe")

    def test_login_with_created_user(self):
        """
        Testa o login com um usuário criado no banco de dados de teste.
        """
        username = 'loginuser'
        password = 'AnotherPass123!'
        User.objects.create_user(username=username, password=password)

        response = self.client.post(self.login_url, {'username': username, 'password': password}, follow=True)
        user = response.context.get('user')
        self.assertIsNotNone(user)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(self.client.login(username=username, password=password))

    def test_login_with_wrong_password(self):
        """
        Testa login com senha incorreta: deve retornar erro.
        """
        username = 'wrongpassuser'
        password = 'CorrectPass123!'
        User.objects.create_user(username=username, password=password)

        response = self.client.post(self.login_url, {'username': username, 'password': 'WrongPass123!'}, follow=True)

        self.assertEqual(response.status_code, 200)
        # Mensagem padrão do Django para login inválido
        self.assertContains(response, "Note que ambos os campos diferenciam maiúsculas e minúsculas.")

class ProtectedViewsTests(TestCase):
    def setUp(self):
        self.username = 'userrestrito'
        self.password = 'SenhaSegura123'
        User.objects.create_user(username=self.username, password=self.password)
        self.dashboard_url = reverse('dashboard')
        self.login_url = reverse('login')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.dashboard_url)
        expected_redirect_url = f"{self.login_url}?next={self.dashboard_url}"
        self.assertRedirects(response, expected_redirect_url)

    def test_access_if_logged_in(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Área restrita")

    def test_access_after_logout(self):
        self.client.login(username=self.username, password=self.password)
        self.client.logout()
        response = self.client.get(self.dashboard_url)
        expected_redirect_url = f"{self.login_url}?next={self.dashboard_url}"
        self.assertRedirects(response, expected_redirect_url)
