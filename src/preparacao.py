"""Pré-processamento e descrição estrutural dos dados - item (a) da ME.

Responsabilidades: conversão de tipos, tratamento de valores ausentes e
documentação da natureza estatística de cada coluna.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import config


def _combinar_data_hora(dados: pd.DataFrame) -> pd.Series:
    """Une 'acq_date' e 'acq_time' em um único timestamp.

    O FIRMS entrega a hora como inteiro no formato HHMM (ex.: 1345, ou 45
    para 00:45). O zfill(4) recompõe os zeros à esquerda que o CSV perdeu ao
    interpretar a coluna como número.
    """
    hora_texto = dados["acq_time"].astype(str).str.zfill(4)
    return pd.to_datetime(
        dados["acq_date"].astype(str) + " " + hora_texto,
        format="%Y-%m-%d %H%M",
        errors="coerce",
    )


def preparar(dados: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Limpa o DataFrame e devolve também o log das decisões de limpeza.

    Retornar o log junto dos dados é intencional: o item (a) exige documentar
    as etapas de pré-processamento, e o relatório é gerado a partir deste
    dicionário em vez de texto escrito à mão.
    """
    registros_originais = len(dados)
    limpo = dados.copy()

    limpo["data_hora"] = _combinar_data_hora(limpo)
    limpo["acq_date"] = pd.to_datetime(limpo["acq_date"], errors="coerce")

    # Timestamps não convertidos indicam formato inesperado em acq_time. Não são
    # motivo para descartar o registro (a análise principal não depende da hora),
    # mas precisam ser contabilizados: se este número for alto, a coluna
    # 'data_hora' não é confiável e a análise temporal deve ser revista.
    timestamps_invalidos = int(limpo["data_hora"].isna().sum())

    # Conversão explícita para numérico: valores inválidos viram NaN em vez de
    # contaminar a coluna com texto e forçar dtype object.
    for coluna in ("frp", "brightness", "confidence", "latitude", "longitude"):
        if coluna in limpo.columns:
            limpo[coluna] = pd.to_numeric(limpo[coluna], errors="coerce")

    # A variável principal não pode ter ausentes: todas as medidas do item (b)
    # dependem dela. Registros sem FRP são descartados e contabilizados.
    ausentes_frp = int(limpo[config.VARIAVEL_NUMERICA].isna().sum())
    limpo = limpo.dropna(subset=[config.VARIAVEL_NUMERICA])

    # FRP igual a zero indica detecção sem energia radiativa mensurável.
    # Mantê-lo distorceria as medidas de tendência central para baixo, por isso
    # é removido — decisão documentada no log para constar no relatório.
    zerados_frp = int((limpo[config.VARIAVEL_NUMERICA] <= 0).sum())
    limpo = limpo[limpo[config.VARIAVEL_NUMERICA] > 0]

    duplicados = int(limpo.duplicated().sum())
    limpo = limpo.drop_duplicates()

    # Normaliza a categórica: espaços e caixa inconsistentes criariam
    # categorias artificiais (ex.: 'Terra' e 'terra ' contadas separadamente).
    if config.VARIAVEL_CATEGORICA in limpo.columns:
        limpo[config.VARIAVEL_CATEGORICA] = (
            limpo[config.VARIAVEL_CATEGORICA].astype(str).str.strip().str.title()
        )

    limpo = limpo.reset_index(drop=True)

    log = {
        "registros_originais": registros_originais,
        "timestamps_nao_convertidos": timestamps_invalidos,
        "removidos_frp_ausente": ausentes_frp,
        "removidos_frp_zero": zerados_frp,
        "removidos_duplicados": duplicados,
        "registros_finais": len(limpo),
        "percentual_retido": round(100 * len(limpo) / registros_originais, 2)
        if registros_originais
        else 0.0,
    }
    return limpo, log


def descrever_estrutura(dados: pd.DataFrame) -> pd.DataFrame:
    """Tabela com tipo, escala de medida e completude de cada coluna.

    Atende diretamente à exigência do item (a): "descreva o tipo de dados
    (dtype), a escala de medida (nominal, de razão, etc.) e o tamanho da
    amostra".
    """
    total = len(dados)
    return pd.DataFrame(
        {
            "coluna": dados.columns,
            "dtype": [str(tipo) for tipo in dados.dtypes],
            "escala_de_medida": [
                config.ESCALAS_DE_MEDIDA.get(coluna, "Não classificada")
                for coluna in dados.columns
            ],
            "valores_preenchidos": [int(dados[c].notna().sum()) for c in dados.columns],
            "valores_ausentes": [int(dados[c].isna().sum()) for c in dados.columns],
            "valores_distintos": [int(dados[c].nunique()) for c in dados.columns],
        }
    ).assign(
        percentual_ausente=lambda tabela: (
            100 * tabela["valores_ausentes"] / total
        ).round(2)
        if total
        else 0.0
    )


def salvar_processado(dados: pd.DataFrame) -> Path:
    """Persiste o dataset limpo, base de todos os cálculos seguintes."""
    config.DIR_DADOS_PROCESSADO.mkdir(parents=True, exist_ok=True)
    destino = config.DIR_DADOS_PROCESSADO / "focos_tratados.csv"
    dados.to_csv(destino, index=False, encoding="utf-8")
    return destino
