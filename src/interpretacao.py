"""Geração do relatório de resultados - itens (a) a (e) da ME.

Camada de apresentação: converte os números calculados pelas outras camadas em
um documento Markdown pronto para ser colado no Google Docs.

IMPORTANTE: este módulo produz as EVIDÊNCIAS QUANTITATIVAS e observações
derivadas diretamente dos dados. A argumentação final do item (e) — os três
insights e as decisões propostas — deve ser escrita por você, com base nessas
evidências. Os trechos marcados com "[ESCREVA AQUI]" indicam onde.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd

import config


def _tabela_markdown(dicionario: dict, col_a: str = "Medida", col_b: str = "Valor") -> str:
    """Converte um dicionário de resultados em tabela Markdown."""
    linhas = [f"| {col_a} | {col_b} |", "| --- | --- |"]
    for chave, valor in dicionario.items():
        if isinstance(valor, float):
            valor_formatado = f"{valor:,.4f}".replace(",", "@").replace(".", ",").replace("@", ".")
        else:
            valor_formatado = str(valor)
        linhas.append(f"| {chave} | {valor_formatado} |")
    return "\n".join(linhas)


def _observacoes_automaticas(resultados: dict) -> list[str]:
    """Extrai observações factuais dos dados, sem interpretá-las.

    A distinção é deliberada: o código só afirma o que os números mostram
    ("a média é X% maior que a mediana"). A conclusão sobre o que isso
    significa no mundo real é trabalho seu — e é exatamente o que o item (e)
    avalia com 0,4 ponto.
    """
    assimetria = resultados["assimetria"]
    outliers = resultados["outliers"]
    moda = resultados["moda"]
    condicional = resultados["condicional"]
    dispersao = resultados["dispersao"]

    razao = assimetria["razão média / mediana"]

    return [
        f"A média ({resultados['central']['média']:.2f} MW) é "
        f"{razao:.2f}x a mediana ({resultados['central']['mediana']:.2f} MW). "
        f"A distribuição foi classificada como {assimetria['interpretação']}, "
        f"com assimetria de {assimetria['assimetria (skewness)']:.2f}.",

        f"O coeficiente de variação é de "
        f"{dispersao['coeficiente de variação (%)']:.1f}%, indicando que o "
        f"desvio padrão ({dispersao['desvio padrão (s)']:.2f} MW) é dessa "
        f"proporção em relação à média — ou seja, a intensidade dos focos é "
        f"altamente heterogênea.",

        f"{outliers['quantidade']} focos ({outliers['percentual (%)']:.2f}% da "
        f"amostra) são outliers pelo critério de Tukey (acima de "
        f"{outliers['limite_superior']:.2f} MW). O foco mais intenso registrado "
        f"atingiu {outliers['maior_valor']:.2f} MW.",

        f"A categoria mais frequente ('{moda['moda']}') concentra "
        f"{moda['frequência_relativa (%)']:.1f}% das detecções "
        f"({moda['frequência_absoluta']} focos).",

        f"Probabilidade condicional: P(A|B) = {condicional['P(A|B)']:.4f} contra "
        f"P(A) = {condicional['P(A)']:.4f}. {condicional['interpretacao']}",
    ]


def gerar_relatorio(resultados: dict) -> Path:
    """Monta o arquivo relatorio/resultados.md com todas as saídas."""
    config.DIR_RELATORIO.mkdir(parents=True, exist_ok=True)
    destino = config.DIR_RELATORIO / "resultados.md"

    log = resultados["log_limpeza"]
    agora = datetime.now().strftime("%d/%m/%Y às %H:%M")

    partes = [
        "# Medida de Eficiência — Big Data (Unidade I)",
        "",
        "**Análise de Focos de Calor no Brasil — NASA FIRMS / EOSDIS**",
        "",
        f"*Relatório gerado automaticamente em {agora}.*",
        "",
        "---",
        "",
        # ---------------------------------------------------------------- (a)
        "## Item (a) — Descrição e Importação dos Dados *(0,3 ponto)*",
        "",
        "### Identificação da fonte",
        "",
        f"- **Órgão:** NASA — *Fire Information for Resource Management System* (FIRMS), "
        f"distribuído pelo EOSDIS/LANCE",
        f"- **Meio de obtenção:** CSV local (sem requisição HTTP em tempo de execução)",
        f"- **Arquivo:** `{resultados['caminho_bruto'].name}`",
        f"- **Portal da fonte original:** {config.PORTAL_FIRMS}",
        f"- **Sensor:** {config.SENSOR} (MODIS, a bordo dos satélites Terra e Aqua)",
        f"- **Recorte espacial:** {config.PAIS} (Brasil)",
        f"- **Recorte temporal:** {resultados.get('periodo', 'coluna acq_date do CSV')}",
        "- **Tema central:** detecção por satélite de focos de calor (queimadas e "
        "incêndios florestais), com medição da potência radiativa liberada.",
        "",
        "### Etapas de pré-processamento aplicadas",
        "",
        _tabela_markdown(log, "Etapa", "Registros"),
        "",
        "Decisões de limpeza e suas justificativas:",
        "",
        "1. **Recomposição do timestamp:** as colunas `acq_date` e `acq_time` "
        "(inteiro no formato HHMM) foram unidas em `data_hora`.",
        "2. **Conversão explícita de tipos:** colunas numéricas convertidas com "
        "`errors='coerce'`, transformando valores inválidos em `NaN` em vez de "
        "forçar a coluna para o tipo `object`.",
        "3. **Remoção de FRP ausente:** registros sem a variável principal foram "
        "descartados, pois inviabilizariam todas as medidas do item (b).",
        "4. **Remoção de FRP igual a zero:** indicam detecção sem energia "
        "radiativa mensurável e deslocariam as medidas de tendência central.",
        "5. **Remoção de duplicatas exatas.**",
        "6. **Normalização da categórica:** `strip()` e `title()` evitam que "
        "variações de grafia criem categorias artificiais.",
        "",
        "### Estrutura das variáveis (dtype, escala de medida e completude)",
        "",
        resultados["estrutura"].to_markdown(index=False),
        "",
        f"**Tamanho final da amostra:** {log['registros_finais']} registros "
        f"({log['registros_finais']} linhas x {resultados['n_colunas']} colunas).",
        "",
        "---",
        "",
        # ---------------------------------------------------------------- (b)
        "## Item (b) — Estatística Descritiva Aprofundada *(0,6 ponto)*",
        "",
        f"- **Variável numérica principal:** `{config.VARIAVEL_NUMERICA}` — "
        f"{config.ROTULO_NUMERICA}",
        f"- **Variável categórica:** `{config.VARIAVEL_CATEGORICA}` — "
        f"{config.ROTULO_CATEGORICA}",
        "",
        "### Medidas de tendência central",
        "",
        _tabela_markdown(resultados["central"]),
        "",
        "### Medidas de dispersão",
        "",
        _tabela_markdown(resultados["dispersao"]),
        "",
        "### Medidas de posição",
        "",
        _tabela_markdown(resultados["posicao"]),
        "",
        "### Análise da variável categórica (moda)",
        "",
        _tabela_markdown(
            {k: v for k, v in resultados["moda"].items() if k != "distribuição_completa"}
        ),
        "",
        "Distribuição de frequências completa:",
        "",
        _tabela_markdown(resultados["moda"]["distribuição_completa"], "Categoria", "Frequência"),
        "",
        "### Justificativa exigida: diferença entre média e mediana",
        "",
        "Diagnóstico quantitativo da forma da distribuição:",
        "",
        _tabela_markdown(resultados["assimetria"]),
        "",
        "Detecção de outliers pelo critério de Tukey (1,5 x IQR):",
        "",
        _tabela_markdown(resultados["outliers"]),
        "",
        "> **[ESCREVA AQUI]** Discuta, com base nos números acima: (i) por que a "
        "média supera a mediana neste conjunto; (ii) o que o desvio padrão "
        "representa concretamente no contexto de intensidade de queimadas; "
        "(iii) qual das duas medidas você usaria para reportar a intensidade "
        "'típica' de um foco e por quê.",
        "",
        "### Comparação da variável numérica entre as categorias",
        "",
        resultados["resumo_categoria"].to_markdown(),
        "",
        "---",
        "",
        # ---------------------------------------------------------------- (c)
        "## Item (c) — Visualização e Análise da Distribuição *(0,4 ponto)*",
        "",
        "Gráficos gerados na pasta `graficos/`:",
        "",
    ]

    for indice, caminho in enumerate(resultados["graficos"], start=1):
        partes.append(f"{indice}. `{caminho.name}`")
    partes += [
        "",
        "- **Gráfico 1** — Box plot + histograma do FRP, com Q1, Q2, Q3 e a média "
        "destacados por linhas verticais (atende à exigência de destacar as "
        "medidas de posição). Escala logarítmica no eixo X, necessária devido à "
        "assimetria da distribuição.",
        "- **Gráfico 2** — Barras da frequência por satélite, com a moda "
        "identificada no título e percentuais sobre as barras.",
        "- **Gráfico 3** — Box plots comparativos do FRP por satélite.",
        "- **Gráfico 4** — Dispersão geográfica (latitude x longitude) com a "
        "intensidade do fogo codificada em cor.",
        "",
        "> **[ESCREVA AQUI]** Descreva o que cada gráfico revela sobre a forma da "
        "distribuição (concentração, cauda, presença de valores extremos).",
        "",
        "---",
        "",
        # ---------------------------------------------------------------- (d)
        "## Item (d) — Probabilidade Simples e Condicional *(0,3 ponto)*",
        "",
        "### Probabilidade simples — P(A)",
        "",
        _tabela_markdown(resultados["simples"]),
        "",
        "### Probabilidade condicional — P(A|B)",
        "",
        _tabela_markdown(resultados["condicional"]),
        "",
        "> **[ESCREVA AQUI]** Explique por que condicionar em B reduz o espaço "
        "amostral e compare P(A|B) com P(A) para concluir se há dependência "
        "entre os eventos.",
        "",
        "---",
        "",
        # ---------------------------------------------------------------- (e)
        "## Item (e) — Interpretação, Insights e Decisão *(0,4 ponto)*",
        "",
        "### Evidências quantitativas extraídas da análise",
        "",
    ]

    for observacao in _observacoes_automaticas(resultados):
        partes.append(f"- {observacao}")

    partes += [
        "",
        "### Os três insights de alto valor",
        "",
        "> **[ESCREVA AQUI — INSIGHT 1]** Formule uma conclusão sobre a "
        "concentração da intensidade dos focos, citando a assimetria e os "
        "outliers como evidência.",
        "",
        "> **[ESCREVA AQUI — INSIGHT 2]** Formule uma conclusão sobre o padrão "
        "temporal (diurno vs. noturno) revelado pela probabilidade condicional.",
        "",
        "> **[ESCREVA AQUI — INSIGHT 3]** Formule uma conclusão sobre a "
        "distribuição geográfica ou sobre a diferença entre os satélites.",
        "",
        "### Decisões organizacionais propostas",
        "",
        "> **[ESCREVA AQUI]** Proponha ações concretas para um órgão como o "
        "IBAMA, ICMBio ou uma secretaria estadual de meio ambiente, usando os "
        "resultados como evidência. Sugestões de direção: priorização de "
        "brigadas nas regiões de maior densidade de focos; dimensionamento de "
        "turnos conforme o padrão diurno/noturno; definição de um limiar de FRP "
        "(por exemplo, o percentil 75) como gatilho automático de alerta "
        "prioritário; alocação orçamentária proporcional à concentração "
        "territorial observada.",
        "",
        "---",
        "",
        "## Reprodutibilidade",
        "",
        f"- Dados brutos preservados em: `{resultados['caminho_bruto'].name}`",
        "- Dados tratados em: `dados/processado/focos_tratados.csv`",
        "- Execução: `python main.py` (ver `README.md`)",
        "",
    ]

    destino.write_text("\n".join(partes), encoding="utf-8")
    return destino
