import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from alimentos.models import PlanoAlimentar


@pytest.mark.django_db
def test_view_plano_list(client):
    user = User.objects.create_user(username="pedro", password="123")
    client.login(username="pedro", password="123")

    url = reverse("plano_list")
    response = client.get(url)

    assert response.status_code == 200
    assert "estrutura" in response.context


@pytest.mark.django_db
def test_view_plano_create(client):
    user = User.objects.create_user(username="pedro", password="123")
    client.login(username="pedro", password="123")

    url = reverse("plano_create")

    data = {
        "dia_semana": "segunda",
        "tipo_refeicao": "cafe",
        "descricao": "Frutas",
        "calorias": 120,
    }

    response = client.post(url, data)

    assert response.status_code == 302
    assert PlanoAlimentar.objects.filter(usuario=user).exists()


@pytest.mark.django_db
def test_view_plano_toggle(client):
    user = User.objects.create_user(username="pedro", password="123")
    client.login(username="pedro", password="123")

    plano = PlanoAlimentar.objects.create(
        usuario=user,
        dia_semana="segunda",
        tipo_refeicao="cafe",
        descricao="Teste",
        calorias=100,
        concluido=False
    )

    url = reverse("plano_toggle", args=[plano.pk])

    response = client.post(url, {"concluido": "on"})

    plano.refresh_from_db()

    assert response.status_code == 302
    assert plano.concluido is True
