import plotly.graph_objects as go
from plotly.offline import plot

def gerar_grafico(planos):
   
    dias = ['segunda', 'terca', 'quarta', 'quinta', 'sexta']


    calorias_diarias = []
    for dia in dias:
        planos_dia = planos.filter(dia_semana=dia, concluido=True)
        total_dia = sum(plano.calorias for plano in planos_dia)
        calorias_diarias.append(total_dia)

    meta_diaria = 1500
    meta_semanal = meta_diaria * len(dias)
    calorias_atingidas = sum(calorias_diarias)
    percentual = (calorias_atingidas / meta_semanal * 100) if meta_semanal else 0

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[dia.capitalize() for dia in dias],
        y=calorias_diarias,
        mode='lines+markers+text',
        line=dict(color="#27ae60", width=4, shape='spline'),
        marker=dict(size=12, color="#2ecc71", line=dict(width=2, color="white")),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.25)',
        name='Calorias diárias',
        text=[f"{y} kcal" for y in calorias_diarias],
        textposition="top center",
        textfont=dict(size=14, color="#2d3436")
    ))


    fig.add_shape(
        type="line",
        x0=0, x1=1, xref="paper",
        y0=meta_diaria, y1=meta_diaria, yref="y",
        line=dict(color="red", width=2, dash="dash"),
    )

    fig.add_annotation(
        text=f"Meta diária: {meta_diaria} kcal",
        xref="paper",
        yref="y",
        x=0.98,
        y=meta_diaria,
        showarrow=False,
        font=dict(size=13, color="red"),
        align="right",
        bgcolor="#ffffff"
    )

   
    fig.update_layout(
        title={
            'text': "Desempenho Semanal de Calorias 🥗",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 26, 'color': '#2d3436'}
        },
        plot_bgcolor='#f9f9f9',
        paper_bgcolor='#ffffff',
        margin=dict(t=80, b=80, l=40, r=40),
        font=dict(family="Arial", size=14, color="#2d3436"),
        showlegend=False,
        yaxis=dict(range=[0, max(max(calorias_diarias), meta_diaria) * 1.3])
    )

    fig.update_yaxes(showgrid=False, zeroline=False, visible=False)
    fig.update_xaxes(
        title="Dias da Semana",
        tickfont=dict(size=16, color="#2d3436", family="Arial Black"),
        showgrid=False
    )

    plot_div = plot(fig, output_type='div', include_plotlyjs=True)

  
    return plot_div, meta_semanal, calorias_atingidas, percentual
