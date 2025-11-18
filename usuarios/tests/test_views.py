import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_view_cadastro_usuario(client):
    url = reverse('signup')  

    data = {
        'username': 'pedro',
        'password1': 'Senha@123',
        'password2': 'Senha@123'
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert User.objects.filter(username='pedro').exists()
