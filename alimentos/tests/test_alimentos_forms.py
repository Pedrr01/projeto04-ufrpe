import pytest
from alimentos.forms import PlanoAlimentarForm


@pytest.mark.django_db
def test_form_plano_valido():
    form = PlanoAlimentarForm(data={
        "dia_semana": "segunda",
        "tipo_refeicao": "cafe",
        "descricao": "Ovos e frutas",
        "calorias": 250,
    })
    assert form.is_valid()


@pytest.mark.django_db
def test_form_plano_faltando_campo():
    form = PlanoAlimentarForm(data={
        "dia_semana": "segunda",
        "tipo_refeicao": "cafe",
        "descricao": "",
        "calorias": 250,
    })
    assert not form.is_valid()
