from django.db import models
from django.contrib.auth.models import User

DIAS_DA_SEMANA = [
    ('segunda', 'Segunda-feira'),
    ('terca', 'Terça-feira'),
    ('quarta', 'Quarta-feira'),
    ('quinta', 'Quinta-feira'),
    ('sexta', 'Sexta-feira'),
]

TIPOS_REFEICAO = [
    ('cafe', 'Café da Manhã'),
    ('almoco', 'Almoço'),
    ('jantar', 'Jantar'),
]

class PlanoAlimentar(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='planos')
    dia_semana = models.CharField(max_length=10, choices=DIAS_DA_SEMANA)
    tipo_refeicao = models.CharField(max_length=10, choices=TIPOS_REFEICAO)
    descricao = models.TextField(verbose_name="Alimentos ou Refeição")

    class Meta:
        unique_together = ('usuario', 'dia_semana', 'tipo_refeicao')
        ordering = ['dia_semana', 'tipo_refeicao']

    def __str__(self):
        return f"{self.get_dia_semana_display()} - {self.get_tipo_refeicao_display()} ({self.usuario.username})"
