# Medida de Eficiência — Big Data (Unidade I)

**Análise de Focos de Calor no Brasil — NASA FIRMS / EOSDIS**

*Relatório gerado automaticamente em 17/09/2026 às 15:33.*

---

## Item (a) — Descrição e Importação dos Dados *(0,3 ponto)*

### Identificação da fonte

- **Órgão:** NASA — *Fire Information for Resource Management System* (FIRMS), distribuído pelo EOSDIS/LANCE
- **Meio de obtenção:** CSV local (sem requisição HTTP em tempo de execução)
- **Arquivo:** `firms_MODIS_NRT_BRA_20260911_211449.csv`
- **Portal da fonte original:** https://firms.modaps.eosdis.nasa.gov/
- **Sensor:** MODIS_NRT (MODIS, a bordo dos satélites Terra e Aqua)
- **Recorte espacial:** BRA (Brasil)
- **Recorte temporal:** 08/09/2026 a 11/09/2026
- **Tema central:** detecção por satélite de focos de calor (queimadas e incêndios florestais), com medição da potência radiativa liberada.

### Etapas de pré-processamento aplicadas

| Etapa | Registros |
| --- | --- |
| registros_originais | 6321 |
| timestamps_nao_convertidos | 0 |
| removidos_frp_ausente | 0 |
| removidos_frp_zero | 0 |
| removidos_duplicados | 0 |
| registros_finais | 6321 |
| percentual_retido | 100,0000 |

Decisões de limpeza e suas justificativas:

1. **Recomposição do timestamp:** as colunas `acq_date` e `acq_time` (inteiro no formato HHMM) foram unidas em `data_hora`.
2. **Conversão explícita de tipos:** colunas numéricas convertidas com `errors='coerce'`, transformando valores inválidos em `NaN` em vez de forçar a coluna para o tipo `object`.
3. **Remoção de FRP ausente:** registros sem a variável principal foram descartados, pois inviabilizariam todas as medidas do item (b).
4. **Remoção de FRP igual a zero:** indicam detecção sem energia radiativa mensurável e deslocariam as medidas de tendência central.
5. **Remoção de duplicatas exatas.**
6. **Normalização da categórica:** `strip()` e `title()` evitam que variações de grafia criem categorias artificiais.

### Estrutura das variáveis (dtype, escala de medida e completude)

| coluna     | dtype          | escala_de_medida                                                |   valores_preenchidos |   valores_ausentes |   valores_distintos |   percentual_ausente |
|:-----------|:---------------|:----------------------------------------------------------------|----------------------:|-------------------:|--------------------:|---------------------:|
| latitude   | float64        | Intervalar (o zero (Equador) é arbitrário, não indica ausência) |                  6321 |                  0 |                6308 |                    0 |
| longitude  | float64        | Intervalar (o zero (Greenwich) é convencional)                  |                  6321 |                  0 |                6309 |                    0 |
| brightness | float64        | De razão (temperatura em Kelvin possui zero absoluto)           |                  6321 |                  0 |                3138 |                    0 |
| scan       | float64        | De razão (tamanho do pixel, zero significa ausência)            |                  6321 |                  0 |                 266 |                    0 |
| track      | float64        | De razão (tamanho do pixel, zero significa ausência)            |                  6321 |                  0 |                 101 |                    0 |
| acq_date   | datetime64[us] | Intervalar (data: diferenças fazem sentido, razões não)         |                  6321 |                  0 |                   4 |                    0 |
| acq_time   | int64          | Intervalar (hora do dia em formato HHMM)                        |                  6321 |                  0 |                 124 |                    0 |
| satellite  | str            | Nominal (Terra / Aqua, sem ordem natural)                       |                  6321 |                  0 |                   2 |                    0 |
| instrument | str            | Nominal (identificação do sensor)                               |                  6321 |                  0 |                   1 |                    0 |
| confidence | int64          | De razão (percentual de 0 a 100 de confiança na detecção)       |                  6321 |                  0 |                  98 |                    0 |
| version    | str            | Nominal (identificador da versão do algoritmo)                  |                  6321 |                  0 |                   1 |                    0 |
| bright_t31 | float64        | De razão (temperatura em Kelvin possui zero absoluto)           |                  6321 |                  0 |                2344 |                    0 |
| frp        | float64        | De razão (potência em MW, zero significa ausência de energia)   |                  6321 |                  0 |                3740 |                    0 |
| daynight   | str            | Nominal dicotômica (D = diurno, N = noturno)                    |                  6321 |                  0 |                   2 |                    0 |
| data_hora  | datetime64[us] | Intervalar (timestamp da detecção)                              |                  6321 |                  0 |                 124 |                    0 |

**Tamanho final da amostra:** 6321 registros (6321 linhas x 15 colunas).

---

## Item (b) — Estatística Descritiva Aprofundada *(0,6 ponto)*

- **Variável numérica principal:** `frp` — FRP - Potência Radiativa do Fogo (MW)
- **Variável categórica:** `satellite` — Satélite de Detecção

### Medidas de tendência central

| Medida | Valor |
| --- | --- |
| média | 41,9582 |
| mediana | 18,1300 |

### Medidas de dispersão

| Medida | Valor |
| --- | --- |
| variância (s²) | 12.467,9016 |
| desvio padrão (s) | 111,6598 |
| coeficiente de variação (%) | 266,1215 |
| amplitude | 3.606,6700 |

### Medidas de posição

| Medida | Valor |
| --- | --- |
| mínimo | 2,5200 |
| Q1 (25%) | 9,7100 |
| Q2 (50% = mediana) | 18,1300 |
| Q3 (75%) | 38,5600 |
| Percentil 75 | 38,5600 |
| máximo | 3.609,1900 |
| IQR (Q3 - Q1) | 28,8500 |

### Análise da variável categórica (moda)

| Medida | Valor |
| --- | --- |
| moda | Aqua |
| é_multimodal | False |
| frequência_absoluta | 4522 |
| frequência_relativa (%) | 71,5393 |

Distribuição de frequências completa:

| Categoria | Frequência |
| --- | --- |
| Aqua | 4522 |
| Terra | 1799 |

### Justificativa exigida: diferença entre média e mediana

Diagnóstico quantitativo da forma da distribuição:

| Medida | Valor |
| --- | --- |
| assimetria (skewness) | 15,2135 |
| curtose | 355,6334 |
| diferença média - mediana | 23,8282 |
| razão média / mediana | 2,3143 |
| interpretação | fortemente assimétrica à direita (cauda longa de valores altos) |

Detecção de outliers pelo critério de Tukey (1,5 x IQR):

| Medida | Valor |
| --- | --- |
| limite_inferior | -33,5650 |
| limite_superior | 81,8350 |
| quantidade | 632 |
| percentual (%) | 9,9984 |
| maior_valor | 3.609,1900 |

> **[ESCREVA AQUI]** Discuta, com base nos números acima: (i) por que a média supera a mediana neste conjunto; (ii) o que o desvio padrão representa concretamente no contexto de intensidade de queimadas; (iii) qual das duas medidas você usaria para reportar a intensidade 'típica' de um foco e por quê.

### Comparação da variável numérica entre as categorias

| satellite   |   contagem |   média |   mediana |   desvio_padrão |   máximo |
|:------------|-----------:|--------:|----------:|----------------:|---------:|
| Aqua        |       4522 |  44.653 |    19.355 |         115.267 |  3609.19 |
| Terra       |       1799 |  35.185 |    15.04  |         101.747 |  1611.78 |

---

## Item (c) — Visualização e Análise da Distribuição *(0,4 ponto)*

Gráficos gerados na pasta `graficos/`:

1. `01_distribuicao_frp_boxplot_histograma.png`
2. `02_frequencia_por_satelite.png`
3. `03_frp_por_satelite.png`
4. `04_dispersao_geografica.png`

- **Gráfico 1** — Box plot + histograma do FRP, com Q1, Q2, Q3 e a média destacados por linhas verticais (atende à exigência de destacar as medidas de posição). Escala logarítmica no eixo X, necessária devido à assimetria da distribuição.
- **Gráfico 2** — Barras da frequência por satélite, com a moda identificada no título e percentuais sobre as barras.
- **Gráfico 3** — Box plots comparativos do FRP por satélite.
- **Gráfico 4** — Dispersão geográfica (latitude x longitude) com a intensidade do fogo codificada em cor.

> **[ESCREVA AQUI]** Descreva o que cada gráfico revela sobre a forma da distribuição (concentração, cauda, presença de valores extremos).

---

## Item (d) — Probabilidade Simples e Condicional *(0,3 ponto)*

### Probabilidade simples — P(A)

| Medida | Valor |
| --- | --- |
| evento | A = o foco selecionado possui FRP acima do percentil 75 |
| valor_de_corte | 38,5600 |
| casos_favoraveis | 1580 |
| espaco_amostral | 6321 |
| P(A) | 0,2500 |
| P(A) em % | 25,0000 |
| valor_teorico_esperado | 0,2500 |

### Probabilidade condicional — P(A|B)

| Medida | Valor |
| --- | --- |
| evento_A | A = a detecção do foco ocorreu no período noturno (daynight = 'N') |
| evento_B | B = o foco possui FRP acima da média da amostra (41.96 MW) |
| P(A) | 0,2245 |
| P(B) | 0,2273 |
| P(A ∩ B) | 0,0380 |
| P(A|B) | 0,1670 |
| P(A|B) em % | 16,7000 |
| espaco_amostral_reduzido | 1437 |
| casos_favoraveis | 240 |
| variacao_vs_P(A) | -0,0575 |
| sao_independentes | False |
| interpretacao | Os eventos são dependentes: a ocorrência de B REDUZ a probabilidade de A em 5.75 pontos percentuais. |

> **[ESCREVA AQUI]** Explique por que condicionar em B reduz o espaço amostral e compare P(A|B) com P(A) para concluir se há dependência entre os eventos.

---

## Item (e) — Interpretação, Insights e Decisão *(0,4 ponto)*

### Evidências quantitativas extraídas da análise

- A média (41.96 MW) é 2.31x a mediana (18.13 MW). A distribuição foi classificada como fortemente assimétrica à direita (cauda longa de valores altos), com assimetria de 15.21.
- O coeficiente de variação é de 266.1%, indicando que o desvio padrão (111.66 MW) é dessa proporção em relação à média — ou seja, a intensidade dos focos é altamente heterogênea.
- 632 focos (10.00% da amostra) são outliers pelo critério de Tukey (acima de 81.84 MW). O foco mais intenso registrado atingiu 3609.19 MW.
- A categoria mais frequente ('Aqua') concentra 71.5% das detecções (4522 focos).
- Probabilidade condicional: P(A|B) = 0.1670 contra P(A) = 0.2245. Os eventos são dependentes: a ocorrência de B REDUZ a probabilidade de A em 5.75 pontos percentuais.

### Os três insights de alto valor

> **[ESCREVA AQUI — INSIGHT 1]** Formule uma conclusão sobre a concentração da intensidade dos focos, citando a assimetria e os outliers como evidência.

> **[ESCREVA AQUI — INSIGHT 2]** Formule uma conclusão sobre o padrão temporal (diurno vs. noturno) revelado pela probabilidade condicional.

> **[ESCREVA AQUI — INSIGHT 3]** Formule uma conclusão sobre a distribuição geográfica ou sobre a diferença entre os satélites.

### Decisões organizacionais propostas

> **[ESCREVA AQUI]** Proponha ações concretas para um órgão como o IBAMA, ICMBio ou uma secretaria estadual de meio ambiente, usando os resultados como evidência. Sugestões de direção: priorização de brigadas nas regiões de maior densidade de focos; dimensionamento de turnos conforme o padrão diurno/noturno; definição de um limiar de FRP (por exemplo, o percentil 75) como gatilho automático de alerta prioritário; alocação orçamentária proporcional à concentração territorial observada.

---

## Reprodutibilidade

- Dados brutos preservados em: `firms_MODIS_NRT_BRA_20260911_211449.csv`
- Dados tratados em: `dados/processado/focos_tratados.csv`
- Execução: `python main.py` (ver `README.md`)
