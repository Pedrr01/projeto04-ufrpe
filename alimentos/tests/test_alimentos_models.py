import pytest
from django.contrib.auth.models import User
from alimentos.models import PlanoAlimentar


@pytest.mark.django_db
def test_plano_alimentar_criacao():
    user = User.objects.create_user(username="pedro", password="123")

    plano = PlanoAlimentar.objects.create(
        usuario=user,
        dia_semana="segunda",
        tipo_refeicao="cafe",
        descricao="Pão e café",
        calorias=300,
        concluido=False
    )

    assert plano.pk is not None
    assert plano.usuario == user
    assert plano.calorias == 300
    assert plano.get_dia_semana_display() == "Segunda-feira"


@pytest.mark.django_db
def test_plano_unique_constraint():
    user = User.objects.create_user(username="pedro", password="123")

    PlanoAlimentar.objects.create(
        usuario=user,
        dia_semana="segunda",
        tipo_refeicao="cafe",
        descricao="Teste",
        calorias=100
    )

    with pytest.raises(Exception):
        # Deve gerar erro por unique_together
        PlanoAlimentar.objects.create(
            usuario=user,
            dia_semana="segunda",
            tipo_refeicao="cafe",
            descricao="Outro",
            calorias=200
        )
