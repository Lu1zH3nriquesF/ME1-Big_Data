"""Gráficos da análise - item (c) da ME (0,4 ponto).

Camada de apresentação. O enunciado exige no mínimo dois gráficos, sendo um
deles com as medidas de posição (quartis) destacadas, e que sejam "claros e
autoexplicativos" — por isso cada figura recebe título, rótulos de eixo com
unidade e legenda com os valores calculados.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import config

# Backend "Agg" renderiza direto em arquivo, sem abrir janela. Necessário para
# o script rodar no terminal do Cursor sem travar esperando interação.
matplotlib.use("Agg")

PALETA = "rocket"
DPI = 150


def configurar_estilo() -> None:
    """Aplica um estilo visual consistente a todas as figuras."""
    sns.set_theme(style="whitegrid", palette=PALETA)
    plt.rcParams.update({
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.bbox": "tight",
        "font.size": 10,
        "axes.titleweight": "bold",
    })


def _salvar(figura: plt.Figure, nome: str) -> Path:
    """Grava a figura em PNG e libera a memória.

    O close() explícito evita o aviso do matplotlib sobre figuras acumuladas,
    que aparece quando muitos gráficos são criados na mesma execução.
    """
    config.DIR_GRAFICOS.mkdir(parents=True, exist_ok=True)
    destino = config.DIR_GRAFICOS / f"{nome}.png"
    figura.savefig(destino)
    plt.close(figura)
    return destino


def grafico_distribuicao_numerica(
    variavel: pd.Series, posicao: dict[str, float]
) -> Path:
    """Histograma + box plot da variável numérica, com os quartis destacados.

    Os dois gráficos compartilham o eixo X e são empilhados de propósito: o
    box plot mostra onde estão os quartis e os outliers, e o histograma logo
    abaixo mostra a forma da distribuição na mesma escala. Assim o leitor
    associa visualmente uma leitura à outra.

    O eixo X usa escala logarítmica porque o FRP é fortemente assimétrico —
    em escala linear, os poucos focos extremos comprimem toda a massa de dados
    contra a esquerda e o gráfico deixa de ser informativo.
    """
    figura, (eixo_box, eixo_hist) = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True,
        gridspec_kw={"height_ratios": [1, 3], "hspace": 0.08},
    )

    sns.boxplot(x=variavel, ax=eixo_box, color="#d95f0e", width=0.5, fliersize=2)
    eixo_box.set(xlabel="", ylabel="")
    eixo_box.set_title(
        f"Distribuição de {config.ROTULO_NUMERICA}\n"
        f"Box plot (topo) e histograma (base) — n = {len(variavel):,} focos".replace(",", "."),
        pad=12,
    )

    sns.histplot(x=variavel, bins=60, ax=eixo_hist, log_scale=True,
                 color="#2c7fb8", edgecolor="white", linewidth=0.3)

    # Linhas verticais nos quartis: é o que atende à exigência explícita do
    # enunciado de "destacar as medidas de posição (Quartis)".
    marcacoes = {
        "Q1 (25%)": (posicao["Q1 (25%)"], "#31a354", "--"),
        "Q2 = Mediana": (posicao["Q2 (50% = mediana)"], "#000000", "-"),
        "Q3 (75%)": (posicao["Q3 (75%)"], "#31a354", "--"),
    }
    for rotulo, (valor, cor, tracejado) in marcacoes.items():
        for eixo in (eixo_box, eixo_hist):
            eixo.axvline(valor, color=cor, linestyle=tracejado, linewidth=1.6,
                         label=f"{rotulo} = {valor:.1f} MW" if eixo is eixo_hist else None)

    media = float(variavel.mean())
    eixo_hist.axvline(media, color="#e34a33", linestyle=":", linewidth=2,
                      label=f"Média = {media:.1f} MW")

    eixo_hist.set_xlabel(f"{config.ROTULO_NUMERICA} — escala logarítmica")
    eixo_hist.set_ylabel("Frequência (nº de focos)")
    eixo_hist.legend(title="Medidas de posição", loc="upper right", framealpha=0.95)

    return _salvar(figura, "01_distribuicao_frp_boxplot_histograma")


def grafico_categorica(variavel: pd.Series) -> Path:
    """Gráfico de barras da variável categórica, com a moda destacada.

    Barras (e não pizza) porque permitem ler a frequência absoluta no eixo e
    comparar categorias por comprimento, que é uma tarefa perceptual mais
    precisa do que comparar ângulos.
    """
    contagem = variavel.value_counts()
    total = int(contagem.sum())

    figura, eixo = plt.subplots(figsize=(9, 5.5))
    barras = sns.barplot(x=contagem.index, y=contagem.values, ax=eixo,
                         hue=contagem.index, legend=False, palette=PALETA)

    # Rótulo com valor absoluto e percentual sobre cada barra: dispensa que o
    # leitor estime a altura, tornando o gráfico autoexplicativo.
    for retangulo, valor in zip(barras.patches, contagem.values):
        eixo.annotate(
            f"{valor:,}".replace(",", ".") + f"\n({100 * valor / total:.1f}%)",
            (retangulo.get_x() + retangulo.get_width() / 2, retangulo.get_height()),
            ha="center", va="bottom", fontsize=9, fontweight="bold",
        )

    eixo.set_title(
        f"Frequência de Focos por {config.ROTULO_CATEGORICA}\n"
        f"Moda = '{contagem.index[0]}' — total de {total:,} focos".replace(",", "."),
        pad=12,
    )
    eixo.set_xlabel(config.ROTULO_CATEGORICA)
    eixo.set_ylabel("Frequência absoluta (nº de focos)")
    eixo.margins(y=0.15)

    return _salvar(figura, "02_frequencia_por_satelite")


def grafico_relacao_categoria_numerica(dados: pd.DataFrame) -> Path:
    """Box plot do FRP separado por categoria: compara as distribuições.

    Gráfico extra (o enunciado pede o mínimo de dois). Serve para sustentar
    com evidência visual o insight de que uma categoria concentra focos mais
    intensos que a outra.
    """
    figura, eixo = plt.subplots(figsize=(9, 5.5))

    sns.boxplot(data=dados, x=config.VARIAVEL_CATEGORICA,
                y=config.VARIAVEL_NUMERICA, ax=eixo, hue=config.VARIAVEL_CATEGORICA,
                legend=False, palette=PALETA, fliersize=2)
    eixo.set_yscale("log")

    eixo.set_title(
        f"Intensidade do Fogo por {config.ROTULO_CATEGORICA}\n"
        "Comparação das distribuições (escala logarítmica)", pad=12,
    )
    eixo.set_xlabel(config.ROTULO_CATEGORICA)
    eixo.set_ylabel(config.ROTULO_NUMERICA)

    return _salvar(figura, "03_frp_por_satelite")


def grafico_dispersao_geografica(dados: pd.DataFrame) -> Path:
    """Dispersão latitude x longitude, com a intensidade do fogo na cor.

    Aproveita a natureza geoespacial da fonte (NASA EOSDIS): o gráfico revela
    a concentração regional dos focos, sustentando recomendações de alocação
    territorial de recursos no item (e).
    """
    figura, eixo = plt.subplots(figsize=(8.5, 8))

    dispersao = eixo.scatter(
        dados["longitude"], dados["latitude"],
        c=dados[config.VARIAVEL_NUMERICA], cmap="inferno_r",
        s=9, alpha=0.6, norm="log",
    )
    figura.colorbar(dispersao, ax=eixo, label=config.ROTULO_NUMERICA, shrink=0.8)

    eixo.set_title(
        f"Distribuição Geográfica dos Focos de Calor — {config.PAIS}\n"
        f"Sensor {config.SENSOR} — extração local em CSV", pad=12,
    )
    eixo.set_xlabel("Longitude (graus)")
    eixo.set_ylabel("Latitude (graus)")
    eixo.set_aspect("equal", adjustable="datalim")

    return _salvar(figura, "04_dispersao_geografica")
