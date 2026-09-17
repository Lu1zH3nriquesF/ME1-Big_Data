"""Orquestrador do pipeline de análise - Medida de Eficiência de Big Data.

Este arquivo não contém regra de negócio: ele apenas coordena as camadas na
ordem correta (coleta -> preparação -> estatística -> gráficos -> relatório).
Ler este arquivo de cima a baixo conta a história completa da análise.

Execução:  python main.py
"""
from __future__ import annotations

import sys

import config
from src import coleta, descritiva, interpretacao, preparacao, probabilidade, visualizacao


def _log(etapa: str, mensagem: str) -> None:
    """Feedback de progresso no terminal."""
    print(f"[{etapa}] {mensagem}")


def executar() -> int:
    """Executa o pipeline completo e devolve o código de saída do processo."""

    # ---------------------------------------------------------------- item (a)
    _log("a", f"Lendo CSV local ({config.ARQUIVO_BRUTO.name})...")
    brutos = coleta.coletar_focos()
    caminho_bruto = coleta.caminho_bruto()
    periodo = coleta.descrever_periodo(brutos)
    _log("a", f"{len(brutos)} registros brutos em {caminho_bruto.name} ({periodo})")

    dados, log_limpeza = preparacao.preparar(brutos)
    preparacao.salvar_processado(dados)
    _log("a", f"{log_limpeza['registros_finais']} registros após limpeza "
              f"({log_limpeza['percentual_retido']}% retidos)")

    if len(dados) < 100:
        _log("!", f"ATENÇÃO: a amostra final tem {len(dados)} registros, abaixo do "
                  "mínimo de 100 exigido pelo enunciado. Substitua o CSV em "
                  "dados/bruto/ por uma extração com mais registros.")

    estrutura = preparacao.descrever_estrutura(dados)

    # ---------------------------------------------------------------- item (b)
    _log("b", "Calculando medidas de tendência central, dispersão e posição...")
    variavel_numerica = dados[config.VARIAVEL_NUMERICA]
    variavel_categorica = dados[config.VARIAVEL_CATEGORICA]

    central = descritiva.medidas_tendencia_central(variavel_numerica)
    dispersao = descritiva.medidas_dispersao(variavel_numerica)
    posicao = descritiva.medidas_posicao(variavel_numerica)
    moda = descritiva.moda_categorica(variavel_categorica)
    assimetria = descritiva.diagnostico_assimetria(variavel_numerica)
    outliers = descritiva.contar_outliers(variavel_numerica)
    resumo_categoria = descritiva.resumo_por_categoria(dados)

    _log("b", f"Média = {central['média']:.2f} MW | "
              f"Mediana = {central['mediana']:.2f} MW | "
              f"Desvio padrão = {dispersao['desvio padrão (s)']:.2f} MW")

    # ---------------------------------------------------------------- item (c)
    _log("c", "Gerando gráficos...")
    visualizacao.configurar_estilo()
    graficos = [
        visualizacao.grafico_distribuicao_numerica(variavel_numerica, posicao),
        visualizacao.grafico_categorica(variavel_categorica),
        visualizacao.grafico_relacao_categoria_numerica(dados),
        visualizacao.grafico_dispersao_geografica(dados),
    ]
    _log("c", f"{len(graficos)} gráficos salvos em graficos/")

    # ---------------------------------------------------------------- item (d)
    _log("d", "Calculando probabilidades simples e condicional...")
    simples = probabilidade.probabilidade_simples(dados)
    condicoes = probabilidade.montar_condicoes_padrao(dados)
    condicional = probabilidade.probabilidade_condicional(
        dados,
        condicoes["condicao_a"],
        condicoes["condicao_b"],
        condicoes["descricao_a"],
        condicoes["descricao_b"],
    )
    _log("d", f"P(A) = {simples['P(A)']} | P(A|B) = {condicional['P(A|B)']}")

    # ---------------------------------------------------------------- item (e)
    _log("e", "Montando relatório de resultados...")
    caminho_relatorio = interpretacao.gerar_relatorio({
        "log_limpeza": log_limpeza,
        "estrutura": estrutura,
        "n_colunas": dados.shape[1],
        "central": central,
        "dispersao": dispersao,
        "posicao": posicao,
        "moda": moda,
        "assimetria": assimetria,
        "outliers": outliers,
        "resumo_categoria": resumo_categoria,
        "graficos": graficos,
        "simples": simples,
        "condicional": condicional,
        "caminho_bruto": caminho_bruto,
        "periodo": periodo,
    })

    print(f"\nConcluído. Relatório: {caminho_relatorio}")
    print("Preencha os trechos marcados com [ESCREVA AQUI] antes de entregar.")
    return 0


def main() -> int:
    """Ponto de entrada com tratamento de erros previstos.

    Erros de coleta e de probabilidade são falhas esperadas de operação (arquivo
    ausente, CSV inválido, condição estatística inválida) e recebem mensagem
    legível em vez de stack trace. Qualquer outra exceção é bug e deve
    propagar normalmente.
    """
    try:
        return executar()
    except coleta.ErroColeta as erro:
        print(f"\nFALHA NA COLETA DE DADOS\n{erro}", file=sys.stderr)
        return 1
    except probabilidade.ErroProbabilidade as erro:
        print(f"\nFALHA NO CÁLCULO DE PROBABILIDADE\n{erro}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
