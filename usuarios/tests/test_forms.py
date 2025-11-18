import pytest
from django.contrib.auth.forms import UserCreationForm

@pytest.mark.django_db
def test_form_usuario_criacao_valido():
    form = UserCreationForm(data={
        'username': 'pedro',
        'password1': 'Senha@123',
        'password2': 'Senha@123',
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_form_usuario_senha_diferente():
    form = UserCreationForm(data={
        'username': 'pedro',
        'password1': 'Senha@123',
        'password2': 'OutraSenha',
    })
    assert not form.is_valid()


@pytest.mark.django_db
def test_form_usuario_username_obrigatorio():
    form = UserCreationForm(data={
        'username': '',
        'password1': 'Senha@123',
        'password2': 'Senha@123',
    })
    assert not form.is_valid()
