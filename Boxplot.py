# coding: utf-8

#        bibliotecas
# -----------------------------
import plotly.graph_objects as plt
from plotly.subplots import make_subplots
# -----------------------------


# Função para plotar boxplot das perdas
def plot_boxplot(data, cenario, variable):

    if cenario == 'monophasic_station':
        x_data = ['20%', '40%', '60%', '80%', '100%']
    else:
        x_data = ['1.0%', '2.0%', '3.0%', '4.0%', '5.0%']
    y_data = data

    colors = ['rgba(213, 228, 207, 0.8)', 'rgba(110, 181, 205, 0.8)',
              'rgba(42, 132, 107, 0.8)', 'rgba(q8, 107, 105, 0.8)', 'rgba(2, 65, 83, 0.8)']
    marker_colors = ['rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)']

    fig = plt.Figure()

    for xd, yd, cls, marker in zip(x_data, y_data, colors, marker_colors):
        fig.add_trace(plt.Box(
            y=yd, name=xd,
            boxpoints='all',
            marker_color=marker, line_color=marker,
            jitter=0.5, whiskerwidth=0.2,
            fillcolor=cls,
            marker_size=3, line_width=1))

    if variable == 'losses':
        fig.update_layout(
            title='Perdas no sistema de distribuição no cenário ' + cenario,
            yaxis_title='Perdas percentuais (%)', xaxis_title='Níveis de Penetração de VEs',
            width=1500, height=750,
            yaxis=dict(
                autorange=True, showgrid=True, zeroline=False,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2,),
            margin=dict(l=40, r=30, b=80, t=100,),
            paper_bgcolor='rgb(255, 255, 255)', plot_bgcolor='rgb(255, 255, 255)',
            showlegend=False)

        if cenario == 'monophasic_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.1,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'triphasic_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.5,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'renewable_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.5,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'stations_mix':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.2,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

    elif variable == 'loading':
        fig.update_layout(
            title='Transformadores em Sobrecarga no cenário ' + cenario,
            yaxis_title='Porcentagem de equipamentos (%)', xaxis_title='Níveis de Penetração de VEs',
            width=1000, height=750,
            yaxis=dict(autorange=True, showgrid=True, zeroline=False,
                       gridcolor='rgb(208, 206, 206)', gridwidth=1,
                       zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2,),
            margin=dict(l=40, r=30, b=80, t=100),
            paper_bgcolor='rgb(255, 255, 255)', plot_bgcolor='rgb(255, 255, 255)',
            showlegend=False)

        if cenario == 'monophasic_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.2,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'triphasic_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.2,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'renewable_station':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.2,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        if cenario == 'stations_mix':
            fig.update_yaxes(
                autorange=True, showgrid=True, zeroline=False,
                dtick=0.2,
                gridcolor='rgb(208, 206, 206)', gridwidth=1,
                zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

    fig.write_image(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\images\fig_" + cenario + "_" + variable + ".pdf")


# Função para plotar boxplot das tensões e dados de carregamento
def plot_double_boxplot(data1, data2, cenario, variable):

    if cenario == 'monophasic_station':
        x_data = ['20%', '40%', '60%', '80%', '100%']
    else:
        x_data = ['1.0%', '2.0%', '3.0%', '4.0%', '5.0%']

    y_data1 = data1
    y_data2 = data2

    colors = ['rgba(213, 228, 207, 0.8)', 'rgba(110, 181, 205, 0.8)',
              'rgba(42, 132, 107, 0.8)', 'rgba(q8, 107, 105, 0.8)', 'rgba(2, 65, 83, 0.8)']
    marker_colors = ['rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)', 'rgb(0,51,0)']

    fig = make_subplots(rows=2, cols=1)

    for xd, yd, cls, marker in zip(x_data, y_data1, colors, marker_colors):
        fig.add_trace(plt.Box(
            y=yd, name=xd, boxpoints='all',
            marker_color=marker, line_color=marker,
            jitter=0.5, whiskerwidth=0.2,
            fillcolor=cls, marker_size=3, line_width=1,),
            row=1, col=1)

    for xd, yd, cls, marker in zip(x_data, y_data2, colors, marker_colors):
        fig.add_trace(plt.Box(
            y=yd, name=xd, boxpoints='all',
            marker_color=marker, line_color=marker,
            jitter=0.5, whiskerwidth=0.2,
            fillcolor=cls, marker_size=3,line_width=1),
            row=2, col=1)

    fig.update_layout(
        title='Limites de tesão observados no SD em (p.u.) no cenário ' + cenario,
        width=1000, height=750,
        yaxis=dict(autorange=True, showgrid=True, zeroline=False,
                   gridcolor='rgb(208, 206, 206)', gridwidth=1,
                   zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2, ),
        margin=dict(l=40, r=30, b=80, t=100),
        paper_bgcolor='rgb(255, 255, 255)', plot_bgcolor='rgb(255, 255, 255)',
        showlegend=False)

    if cenario == 'monophasic_station':
        fig.update_yaxes(
            title_text="Tensão Mínima",
            row=2, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.002,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=1, col=1)

        fig.add_hline(y=1.05, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Superior de Operação",
                      row=1, col=1)

        fig.update_yaxes(
            title_text="Tensão Máxima",
            row=1, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.002,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=2, col=1)

        fig.add_hline(y=0.92, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Inferior de Operação",
                      row=2, col=1)

    elif cenario == 'triphasic_station':
        fig.update_yaxes(
            title_text="Tensão Mínima",
            row=2, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.01,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=1, col=1)

        fig.add_hline(y=1.05, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Superior de Operação",
                      row=1, col=1)

        fig.update_yaxes(
            title_text="Tensão Máxima",
            row=1, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.005,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=2, col=1)

        fig.add_hline(y=0.92, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Inferior de Operação",
                      row=2, col=1)

    elif cenario == 'renewable_station':
        fig.update_yaxes(
            title_text="Tensão Mínima",
            row=2, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.01,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=1, col=1)

        fig.add_hline(y=1.05, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Superior de Operação",
                      row=1, col=1)

        fig.update_yaxes(
            title_text="Tensão Máxima",
            row=1, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.005,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=2, col=1)

        fig.add_hline(y=0.92, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Inferior de Operação",
                      row=2, col=1)

    elif cenario == 'stations_mix':
        fig.update_yaxes(
            title_text="Tensão Mínima",
            row=2, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.01,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=1, col=1)

        fig.add_hline(y=1.05, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Superior de Operação",
                      row=1, col=1)

        fig.update_yaxes(
            title_text="Tensão Máxima",
            row=1, col=1,
            autorange=True, showgrid=True, zeroline=False,
            dtick=0.005,
            gridcolor='rgb(208, 206, 206)', gridwidth=1,
            zerolinecolor='rgb(0, 0, 0)', zerolinewidth=2)

        fig.update_xaxes(title='Níveis de Penetração de VEs', row=2, col=1)

        fig.add_hline(y=0.92, line_dash="dash", name='teste',
                      line=dict(color='black', width=2),
                      annotation_text="Limite Inferior de Operação",
                      row=2, col=1)

    fig.write_image(r"D:\Pedro\Universidade\TCC\Simulacoes\Teste_DLL\images\fig_" + cenario + "_" + variable + ".pdf")
