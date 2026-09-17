"""Validação do pipeline com dados sintéticos, sem o CSV real.

Por que isso existe: a camada de domínio (descritiva, probabilidade) não conhece
a origem dos dados. Logo, é possível verificar que todos os cálculos e gráficos
funcionam sem o arquivo bruto — basta injetar um DataFrame com o mesmo formato
que o CSV do FIRMS.

Os dados aqui são FICTÍCIOS e servem apenas para teste técnico. Nunca use estes
resultados no relatório final.

Execução:  python validar_pipeline.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import config
from src import descritiva, interpretacao, preparacao, probabilidade, visualizacao

SEMENTE = 42
N_REGISTROS = 800
N_DIAS_SINTETICOS = 5


def gerar_dados_ficticios() -> pd.DataFrame:
    """Cria um DataFrame com o mesmo esquema do CSV do FIRMS/MODIS.

    O FRP é gerado por distribuição lognormal porque é assim que a intensidade
    de queimadas se comporta na realidade: muitos focos fracos e poucos focos
    extremamente intensos. Isso garante que o teste exercite os mesmos caminhos
    de código que os dados reais (assimetria, outliers, escala logarítmica).
    """
    aleatorio = np.random.default_rng(SEMENTE)

    frp = aleatorio.lognormal(mean=2.5, sigma=1.1, size=N_REGISTROS).round(2)

    # Introduz valores inválidos de propósito para exercitar a limpeza.
    frp[aleatorio.choice(N_REGISTROS, 15, replace=False)] = 0.0
    frp[aleatorio.choice(N_REGISTROS, 10, replace=False)] = np.nan

    datas = pd.date_range("2026-09-04", periods=N_DIAS_SINTETICOS, freq="D")

    # O FIRMS codifica a hora como inteiro HHMM, então os minutos vão apenas de
    # 0 a 59. Sortear um inteiro qualquer entre 0 e 2359 produziria horários
    # impossíveis (ex.: 1375 = "13h75"), que virariam NaT na conversão.
    horas = aleatorio.integers(0, 24, N_REGISTROS)
    minutos = aleatorio.integers(0, 60, N_REGISTROS)

    return pd.DataFrame({
        "latitude": aleatorio.uniform(-33.0, 5.0, N_REGISTROS).round(4),
        "longitude": aleatorio.uniform(-74.0, -34.0, N_REGISTROS).round(4),
        "brightness": aleatorio.normal(325, 18, N_REGISTROS).round(1),
        "scan": aleatorio.uniform(1.0, 2.5, N_REGISTROS).round(2),
        "track": aleatorio.uniform(1.0, 1.8, N_REGISTROS).round(2),
        "acq_date": aleatorio.choice(datas.strftime("%Y-%m-%d"), N_REGISTROS),
        "acq_time": horas * 100 + minutos,
        "satellite": aleatorio.choice(["Terra", "Aqua"], N_REGISTROS, p=[0.55, 0.45]),
        "instrument": "MODIS",
        "confidence": aleatorio.integers(0, 101, N_REGISTROS),
        "version": "6.1NRT",
        "bright_t31": aleatorio.normal(295, 10, N_REGISTROS).round(1),
        "frp": frp,
        "daynight": aleatorio.choice(["D", "N"], N_REGISTROS, p=[0.7, 0.3]),
        "country_id": "BRA",
    })


def main() -> int:
    print("=" * 70)
    print("VALIDAÇÃO COM DADOS SINTÉTICOS — resultados não servem ao relatório")
    print("=" * 70)

    brutos = gerar_dados_ficticios()
    print(f"\n[a] {len(brutos)} registros fictícios gerados")

    dados, log = preparacao.preparar(brutos)
    print(f"[a] Limpeza: {log}")

    estrutura = preparacao.descrever_estrutura(dados)
    print(f"[a] Estrutura descrita para {len(estrutura)} colunas")

    variavel_numerica = dados[config.VARIAVEL_NUMERICA]
    variavel_categorica = dados[config.VARIAVEL_CATEGORICA]

    central = descritiva.medidas_tendencia_central(variavel_numerica)
    dispersao = descritiva.medidas_dispersao(variavel_numerica)
    posicao = descritiva.medidas_posicao(variavel_numerica)
    moda = descritiva.moda_categorica(variavel_categorica)
    assimetria = descritiva.diagnostico_assimetria(variavel_numerica)
    outliers = descritiva.contar_outliers(variavel_numerica)
    resumo_categoria = descritiva.resumo_por_categoria(dados)

    print(f"[b] Média={central['média']:.2f} Mediana={central['mediana']:.2f} "
          f"s={dispersao['desvio padrão (s)']:.2f}")
    print(f"[b] Q1={posicao['Q1 (25%)']:.2f} Q2={posicao['Q2 (50% = mediana)']:.2f} "
          f"Q3={posicao['Q3 (75%)']:.2f}")
    print(f"[b] Moda='{moda['moda']}' ({moda['frequência_relativa (%)']:.1f}%)")
    print(f"[b] Assimetria={assimetria['assimetria (skewness)']:.2f} "
          f"({assimetria['interpretação']})")
    print(f"[b] Outliers: {outliers['quantidade']} ({outliers['percentual (%)']:.2f}%)")

    visualizacao.configurar_estilo()
    graficos = [
        visualizacao.grafico_distribuicao_numerica(variavel_numerica, posicao),
        visualizacao.grafico_categorica(variavel_categorica),
        visualizacao.grafico_relacao_categoria_numerica(dados),
        visualizacao.grafico_dispersao_geografica(dados),
    ]
    for caminho in graficos:
        print(f"[c] Gráfico gerado: {caminho.name}")

    simples = probabilidade.probabilidade_simples(dados)
    condicoes = probabilidade.montar_condicoes_padrao(dados)
    condicional = probabilidade.probabilidade_condicional(
        dados, condicoes["condicao_a"], condicoes["condicao_b"],
        condicoes["descricao_a"], condicoes["descricao_b"],
    )
    print(f"[d] P(A)={simples['P(A)']} (teórico {simples['valor_teorico_esperado']})")
    print(f"[d] P(A|B)={condicional['P(A|B)']} vs P(A)={condicional['P(A)']}")

    caminho = interpretacao.gerar_relatorio({
        "log_limpeza": log, "estrutura": estrutura, "n_colunas": dados.shape[1],
        "central": central, "dispersao": dispersao, "posicao": posicao,
        "moda": moda, "assimetria": assimetria, "outliers": outliers,
        "resumo_categoria": resumo_categoria, "graficos": graficos,
        "simples": simples, "condicional": condicional,
        "caminho_bruto": config.DIR_DADOS_BRUTO / "SINTETICO.csv",
        "periodo": "dados sintéticos (não usar no relatório)",
    })
    print(f"[e] Relatório gerado: {caminho}")

    print("\nVALIDAÇÃO CONCLUÍDA — pipeline funcional.")
    print("Execute 'python main.py' para analisar o CSV em dados/bruto/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
