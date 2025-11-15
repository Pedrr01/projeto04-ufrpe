# alimentos/views.py
from io import BytesIO

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from .models import PlanoAlimentar
from .forms import PlanoAlimentarForm
from .estatisticas import gerar_grafico


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

    plot_div, meta_semanal, calorias_atingidas, percentual = gerar_grafico(planos)

    return render(request, 'tempAlimentos/plano_estatisticas.html', {
        'total_refeicoes': total_refeicoes,
        'total_concluidas': total_concluidas,
        'plot_div': plot_div,
        'meta_semanal': meta_semanal,
        'calorias_atingidas': calorias_atingidas,
        'percentual': percentual,
    })


# ----------------------------
# Funções para gerar PDFs
# ----------------------------

@login_required
def plano_download_pdf(request):
    """
    Gera PDF com o plano alimentar da semana do usuário.
    """
    planos = PlanoAlimentar.objects.filter(usuario=request.user).order_by('dia_semana', 'tipo_refeicao')
    dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(2 * cm, y, f"Plano Alimentar - {request.user.username}")
    y -= 1 * cm

    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]

    for dia in dias:
        # título do dia
        p.setFont("Helvetica-Bold", 14)
        p.setFillColor(colors.HexColor("#EF5350"))
        p.drawString(2 * cm, y, f"{dia.capitalize()}")
        y -= 0.6 * cm

        # construir tabela do dia
        data = [["Refeição", "Descrição", "Calorias", "Concluído"]]
        planos_dia = planos.filter(dia_semana=dia)
        for plano in planos_dia:
            descricao_par = Paragraph(plano.descricao.replace("\n", "<br/>"), styleN)
            data.append([
                plano.get_tipo_refeicao_display(),
                descricao_par,
                f"{plano.calorias} kcal",
                "✅" if plano.concluido else "❌"
            ])

        if len(data) > 1:
            # desenhar tabela
            table = Table(data, colWidths=[3 * cm, 9 * cm, 3 * cm, 2 * cm])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EF5350")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('GRID', (0, 0), (-1, -1), 0.25, colors.gray),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (1, 1), (1, -1), 6),
                ('RIGHTPADDING', (1, 1), (1, -1), 6),
            ]))
            w, h = table.wrapOn(p, width - 4 * cm, y)
            # se não couber na página, criar nova página
            if y - h < 2 * cm:
                p.showPage()
                y = height - 2 * cm
            table.drawOn(p, 2 * cm, y - h)
            y = y - h - 1 * cm
        else:
            p.setFont("Helvetica", 12)
            p.setFillColor(colors.black)
            p.drawString(2 * cm, y, "Nenhuma refeição cadastrada.")
            y -= 1 * cm

        if y < 4 * cm:
            p.showPage()
            y = height - 2 * cm

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="plano_alimentar.pdf"'
    return response


@login_required
def plano_estatisticas_pdf(request):
    """
    Gera PDF com as estatísticas do plano.
    Observação: por simplicidade este PDF inclui o resumo textual.
    Podemos também inserir o gráfico (como imagem) se quiser.
    """
    planos = PlanoAlimentar.objects.filter(usuario=request.user)
    total_refeicoes = planos.count()
    total_concluidas = planos.filter(concluido=True).count()
    _, meta_semanal, calorias_atingidas, percentual = gerar_grafico(planos)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 3 * cm

    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.HexColor("#27ae60"))
    p.drawString(2 * cm, y, f"Estatísticas - {request.user.username}")
    y -= 1.5 * cm

    p.setFont("Helvetica", 13)
    p.setFillColor(colors.black)
    stats = [
        ("Total de refeições", total_refeicoes),
        ("Concluídas", total_concluidas),
        ("Meta semanal", f"{meta_semanal} kcal"),
        ("Atingido", f"{calorias_atingidas} kcal"),
        ("Progresso", f"{percentual:.1f}%"),
    ]
    for label, value in stats:
        p.drawString(2 * cm, y, f"{label}: {value}")
        y -= 1 * cm

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="estatisticas_plano.pdf"'
    return response
