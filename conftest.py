import pytest
from django.contrib.auth.models import User
from alimentos.models import PlanoAlimentar

@pytest.fixture
def usuario():
    return User.objects.create_user(
        username='pedro',
        password='123456'
    )

@pytest.fixture
def plano(usuario):
    return PlanoAlimentar.objects.create(
        usuario=usuario,
        dia_semana='segunda',
        tipo_refeicao='almoco',
        descricao='Arroz, frango e salada',
        calorias=650,
        concluido=False
    )
