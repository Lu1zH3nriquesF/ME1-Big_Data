"""Importação dos focos de calor a partir de CSV local - item (a) da ME.

Camada de infraestrutura: é o único módulo que conhece o sistema de arquivos.
Os módulos de estatística recebem apenas um DataFrame já pronto, sem saber de
onde ele veio. Essa inversão de dependência permite testar os cálculos com
dados fictícios, sem o arquivo bruto.

Este módulo NÃO faz requisição HTTP. A origem intelectual dos dados continua
sendo o NASA FIRMS; o meio de obtenção é o CSV persistido em dados/bruto/.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import config


class ErroColeta(RuntimeError):
    """Falha ao ler o CSV local.

    Exceção própria para que o orquestrador (main.py) distinga um problema de
    importação de um erro de programação, exibindo mensagem útil ao usuário.
    """


def caminho_bruto() -> Path:
    """Caminho do CSV que alimenta o pipeline — a fonte única em disco."""
    return config.ARQUIVO_BRUTO


def descrever_periodo(dados: pd.DataFrame) -> str:
    """Extrai o intervalo real de datas do próprio CSV.

    O recorte temporal não é mais um parâmetro de API: ele está nas linhas.
    Se a coluna não puder ser interpretada, devolvemos uma mensagem honesta
    em vez de inventar um número de dias.
    """
    if "acq_date" not in dados.columns:
        return "período não identificado (coluna acq_date ausente)"

    datas = pd.to_datetime(dados["acq_date"], errors="coerce")
    validas = datas.dropna()
    if validas.empty:
        return "período não identificado (datas inválidas em acq_date)"

    inicio = validas.min().strftime("%d/%m/%Y")
    fim = validas.max().strftime("%d/%m/%Y")
    return f"{inicio} a {fim}"


def coletar_focos() -> pd.DataFrame:
    """Lê o CSV local e devolve um DataFrame, sem qualquer chamada de rede.

    As checagens de arquivo ausente, tabela vazia e colunas obrigatórias
    substituem as antigas falhas de HTTP: o esquema do FIRMS continua sendo
    validado, só que contra o disco em vez do servidor.
    """
    caminho = caminho_bruto()

    if not caminho.is_file():
        raise ErroColeta(
            f"CSV bruto não encontrado em {caminho}.\n"
            "  Coloque o arquivo do FIRMS em dados/bruto/ e atualize "
            "config.ARQUIVO_BRUTO com o nome correto."
        )

    try:
        dados = pd.read_csv(caminho)
    except pd.errors.ParserError as erro:
        raise ErroColeta(
            f"O arquivo {caminho.name} não pôde ser lido como CSV.\n"
            f"  Detalhe: {erro}"
        ) from erro
    except OSError as erro:
        raise ErroColeta(
            f"Falha ao abrir {caminho.name}: {erro}"
        ) from erro

    if dados.empty:
        raise ErroColeta(
            f"O CSV {caminho.name} está vazio (nenhum foco para analisar). "
            "Substitua-o por uma extração com mais registros."
        )

    faltantes = set(config.COLUNAS_OBRIGATORIAS) - set(dados.columns)
    if faltantes:
        raise ErroColeta(
            f"O CSV não contém as colunas esperadas: {sorted(faltantes)}. "
            f"Colunas recebidas: {list(dados.columns)}"
        )

    return dados
