from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PlanoAlimentar
from .forms import PlanoAlimentarForm
from django.shortcuts import get_object_or_404

@login_required
def plano_list(request):
    planos = PlanoAlimentar.objects.filter(usuario=request.user)
    dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']
    refeicoes = ['cafe', 'almoco', 'jantar']

    estrutura = {dia: {ref: None for ref in refeicoes} for dia in dias}
    for plano in planos:
        estrutura[plano.dia_semana][plano.tipo_refeicao] = plano

    return render(request, 'tempAlimentos/plano_list.html', {'estrutura': estrutura})

@login_required
def plano_create(request):
    if request.method == 'POST':
        form = PlanoAlimentarForm(request.POST)
        if form.is_valid():
            plano = form.save(commit=False)
            plano.usuario = request.user
            plano.save()
            return redirect('plano_list')
    else:
        form = PlanoAlimentarForm()
    return render(request, 'tempAlimentos/plano_form.html', {'form': form})

@login_required
def plano_toggle(request, pk):
    plano = get_object_or_404(PlanoAlimentar, pk=pk, usuario=request.user)
    if request.method == "POST":
        plano.concluido = not plano.concluido
        plano.save()
    return redirect('plano_list')

@login_required
def plano_estatisticas(request):
    planos = PlanoAlimentar.objects.filter(usuario=request.user)
    total_refeicoes = planos.count()
    total_concluidas = planos.filter(concluido=True).count()
    return render(request, 'tempAlimentos/plano_estatisticas.html', {
        'total_refeicoes': total_refeicoes,
        'total_concluidas': total_concluidas
    })