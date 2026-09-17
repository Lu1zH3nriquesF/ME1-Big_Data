"""Probabilidade simples e condicional - item (d) da ME.

Camada de domínio. Todas as probabilidades são estimadas pela abordagem
FREQUENTISTA: a razão entre casos favoráveis e o total de observações da
amostra. Não há suposição de distribuição teórica.
"""
from __future__ import annotations

import pandas as pd

import config


class ErroProbabilidade(ValueError):
    """Condição inválida para cálculo de probabilidade."""


def probabilidade_simples(dados: pd.DataFrame) -> dict[str, object]:
    """P(A): probabilidade de um foco aleatório estar acima do percentil 75.

    Conceito: o percentil 75 corta a distribuição de modo que 75% dos valores
    fiquem abaixo dele. Logo, o resultado teórico esperado é ~0,25.

    O valor empírico raramente é exatamente 0,25 — quando há valores repetidos
    exatamente no ponto de corte, a proporção se desloca. Essa diferença é um
    ótimo ponto de discussão no relatório.
    """
    variavel = dados[config.VARIAVEL_NUMERICA]
    corte = float(variavel.quantile(config.PERCENTIL_ALVO))

    casos_favoraveis = int((variavel > corte).sum())
    total = len(variavel)

    if total == 0:
        raise ErroProbabilidade("Não há registros para calcular a probabilidade.")

    probabilidade = casos_favoraveis / total

    return {
        "evento": (
            f"A = o foco selecionado possui {config.VARIAVEL_NUMERICA.upper()} "
            f"acima do percentil {int(config.PERCENTIL_ALVO * 100)}"
        ),
        "valor_de_corte": round(corte, 3),
        "casos_favoraveis": casos_favoraveis,
        "espaco_amostral": total,
        "P(A)": round(probabilidade, 4),
        "P(A) em %": round(100 * probabilidade, 2),
        "valor_teorico_esperado": round(1 - config.PERCENTIL_ALVO, 4),
    }


def probabilidade_condicional(
    dados: pd.DataFrame,
    condicao_a: pd.Series,
    condicao_b: pd.Series,
    descricao_a: str,
    descricao_b: str,
) -> dict[str, object]:
    """P(A|B) = P(A ∩ B) / P(B): probabilidade de A dado que B ocorreu.

    Conceito central: condicionar REDUZ o espaço amostral. Em vez de olhar
    todos os focos, olhamos apenas o subconjunto onde B é verdadeiro, e dentro
    dele medimos a proporção de A.

    Recebe as condições como máscaras booleanas (e não como strings de query)
    para que a função permaneça genérica e testável, sem interpretar sintaxe.
    """
    total = len(dados)
    ocorrencias_b = int(condicao_b.sum())

    if ocorrencias_b == 0:
        raise ErroProbabilidade(
            f"A condição B ({descricao_b}) nunca ocorre na amostra. "
            "P(A|B) é indefinida porque exigiria divisão por zero."
        )

    ocorrencias_a = int(condicao_a.sum())
    intersecao = int((condicao_a & condicao_b).sum())

    p_a = ocorrencias_a / total
    p_b = ocorrencias_b / total
    p_a_dado_b = intersecao / ocorrencias_b

    # Se P(A|B) == P(A), a ocorrência de B não altera a chance de A: os eventos
    # são independentes. Qualquer desvio indica associação entre as variáveis,
    # que é justamente o achado relevante para o relatório.
    diferenca = p_a_dado_b - p_a

    return {
        "evento_A": descricao_a,
        "evento_B": descricao_b,
        "P(A)": round(p_a, 4),
        "P(B)": round(p_b, 4),
        "P(A ∩ B)": round(intersecao / total, 4),
        "P(A|B)": round(p_a_dado_b, 4),
        "P(A|B) em %": round(100 * p_a_dado_b, 2),
        "espaco_amostral_reduzido": ocorrencias_b,
        "casos_favoraveis": intersecao,
        "variacao_vs_P(A)": round(diferenca, 4),
        "sao_independentes": abs(diferenca) < 0.01,
        "interpretacao": _interpretar_dependencia(diferenca),
    }


def _interpretar_dependencia(diferenca: float) -> str:
    """Traduz a diferença entre P(A|B) e P(A) em linguagem natural."""
    if abs(diferenca) < 0.01:
        return (
            "Os eventos são praticamente independentes: saber que B ocorreu "
            "não altera a probabilidade de A."
        )
    tendencia = "AUMENTA" if diferenca > 0 else "REDUZ"
    return (
        f"Os eventos são dependentes: a ocorrência de B {tendencia} a "
        f"probabilidade de A em {abs(diferenca) * 100:.2f} pontos percentuais."
    )


def montar_condicoes_padrao(dados: pd.DataFrame) -> dict[str, tuple]:
    """Constrói o par de condições sugerido pelo enunciado do item (d).

    O exemplo do enunciado é "probabilidade de ser do sexo X, dado que a
    coluna Y é maior que a média". A tradução para este dataset:
      A = a detecção é noturna (daynight == 'N')
      B = o FRP do foco está acima da média

    A pergunta de negócio resultante: focos mais intensos que a média tendem a
    ser detectados à noite? Isso tem implicação operacional direta no
    dimensionamento de turnos de brigadas de incêndio.
    """
    media_frp = dados[config.VARIAVEL_NUMERICA].mean()

    condicao_a = dados["daynight"].astype(str).str.upper().str.startswith("N")
    condicao_b = dados[config.VARIAVEL_NUMERICA] > media_frp

    return {
        "condicao_a": condicao_a,
        "condicao_b": condicao_b,
        "descricao_a": "A = a detecção do foco ocorreu no período noturno (daynight = 'N')",
        "descricao_b": (
            f"B = o foco possui FRP acima da média da amostra "
            f"({media_frp:.2f} MW)"
        ),
    }
