"""Estatística descritiva - item (b) da ME, o de maior peso (0,6 ponto).

Camada de domínio: funções puras que recebem Series/DataFrame e devolvem
números. Não leem arquivos, não acessam rede e não desenham gráficos, o que
permite validá-las com dados fictícios.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config


def medidas_tendencia_central(variavel: pd.Series) -> dict[str, float]:
    """Média e mediana da variável numérica.

    A média usa todos os valores e por isso é sensível a outliers; a mediana
    é a posição central e resiste a eles. Comparar as duas revela a assimetria
    da distribuição, análise exigida na justificativa do item (b).
    """
    return {
        "média": float(variavel.mean()),
        "mediana": float(variavel.median()),
    }


def medidas_dispersao(variavel: pd.Series) -> dict[str, float]:
    """Variância e desvio padrão AMOSTRAIS (ddof=1).

    ddof=1 aplica a correção de Bessel (divide por n-1, não por n), correta
    porque os focos coletados são uma AMOSTRA do total de queimadas, não a
    população inteira. O pandas usa ddof=1 por padrão, mas o numpy usa ddof=0 —
    o parâmetro é explicitado para deixar a escolha estatística documentada.
    """
    return {
        "variância (s²)": float(variavel.var(ddof=1)),
        "desvio padrão (s)": float(variavel.std(ddof=1)),
        "coeficiente de variação (%)": float(
            100 * variavel.std(ddof=1) / variavel.mean()
        ),
        "amplitude": float(variavel.max() - variavel.min()),
    }


def medidas_posicao(variavel: pd.Series) -> dict[str, float]:
    """Quartis (Q1, Q2, Q3), percentil 75 e amplitude interquartil.

    Q3 e o percentil 75 são matematicamente o mesmo valor; ambos aparecem
    porque o enunciado os pede nominalmente em itens distintos.
    """
    q1, q2, q3 = (float(variavel.quantile(p)) for p in (0.25, 0.50, 0.75))
    return {
        "mínimo": float(variavel.min()),
        "Q1 (25%)": q1,
        "Q2 (50% = mediana)": q2,
        "Q3 (75%)": q3,
        f"Percentil {int(config.PERCENTIL_ALVO * 100)}": float(
            variavel.quantile(config.PERCENTIL_ALVO)
        ),
        "máximo": float(variavel.max()),
        "IQR (Q3 - Q1)": q3 - q1,
    }


def moda_categorica(variavel: pd.Series) -> dict[str, object]:
    """Moda da variável qualitativa: a categoria mais frequente.

    Média e mediana não fazem sentido em escala nominal (não há ordem nem
    distância entre 'Terra' e 'Aqua'), por isso a moda é a única medida de
    tendência central aplicável aqui.
    """
    modas = variavel.mode()
    contagem = variavel.value_counts()

    return {
        "moda": modas.iloc[0] if not modas.empty else None,
        "é_multimodal": len(modas) > 1,
        "frequência_absoluta": int(contagem.iloc[0]) if not contagem.empty else 0,
        "frequência_relativa (%)": float(
            100 * contagem.iloc[0] / len(variavel)
        ) if not contagem.empty else 0.0,
        "distribuição_completa": contagem.to_dict(),
    }


def diagnostico_assimetria(variavel: pd.Series) -> dict[str, object]:
    """Quantifica a assimetria para embasar a discussão média vs. mediana.

    Não é exigido pelo enunciado, mas transforma a justificativa do item (b)
    de uma afirmação qualitativa em uma conclusão medida. Regra de bolso:
    |assimetria| > 1 indica distribuição fortemente assimétrica.
    """
    media, mediana = float(variavel.mean()), float(variavel.median())
    assimetria = float(variavel.skew())

    if assimetria > 1:
        formato = "fortemente assimétrica à direita (cauda longa de valores altos)"
    elif assimetria > 0.5:
        formato = "moderadamente assimétrica à direita"
    elif assimetria < -1:
        formato = "fortemente assimétrica à esquerda"
    elif assimetria < -0.5:
        formato = "moderadamente assimétrica à esquerda"
    else:
        formato = "aproximadamente simétrica"

    return {
        "assimetria (skewness)": assimetria,
        "curtose": float(variavel.kurt()),
        "diferença média - mediana": media - mediana,
        "razão média / mediana": media / mediana if mediana else np.nan,
        "interpretação": formato,
    }


def contar_outliers(variavel: pd.Series) -> dict[str, object]:
    """Identifica outliers pelo critério de Tukey (1,5 x IQR).

    É o mesmo critério que o box plot do item (c) usa para desenhar os pontos
    fora dos "bigodes"; calculá-lo aqui permite citar o número exato no texto
    em vez de apenas apontar para o gráfico.
    """
    q1, q3 = variavel.quantile(0.25), variavel.quantile(0.75)
    iqr = q3 - q1
    limite_inferior, limite_superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    outliers = variavel[(variavel < limite_inferior) | (variavel > limite_superior)]

    return {
        "limite_inferior": float(limite_inferior),
        "limite_superior": float(limite_superior),
        "quantidade": int(len(outliers)),
        "percentual (%)": float(100 * len(outliers) / len(variavel)),
        "maior_valor": float(variavel.max()),
    }


def resumo_por_categoria(dados: pd.DataFrame) -> pd.DataFrame:
    """Cruza a variável numérica com a categórica.

    Base do primeiro insight do item (e): permite afirmar se um satélite
    detecta focos sistematicamente mais intensos que o outro.
    """
    return (
        dados.groupby(config.VARIAVEL_CATEGORICA, observed=True)[
            config.VARIAVEL_NUMERICA
        ]
        .agg(
            contagem="count",
            média="mean",
            mediana="median",
            desvio_padrão=lambda serie: serie.std(ddof=1),
            máximo="max",
        )
        .round(3)
    )
