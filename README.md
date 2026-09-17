# ME — Big Data (Unidade I): Análise de Focos de Calor via NASA FIRMS

Ciclo completo de análise de dados em Python, da coleta ao insight, sobre
detecções de focos de calor no Brasil obtidas do **FIRMS** (*Fire Information
for Resource Management System*), serviço da NASA distribuído pelo **EOSDIS**.

## Fonte dos dados

| Item | Valor |
| --- | --- |
| Órgão | NASA — FIRMS / EOSDIS / LANCE |
| Portal | https://firms.modaps.eosdis.nasa.gov/ |
| Meio de obtenção | CSV local em `dados/bruto/` (sem requisição HTTP) |
| Sensor | MODIS (satélites Terra e Aqua) |
| Formato | CSV (lido pelo `pandas`) |

A escolha do FIRMS dentro do EOSDIS é deliberada: os produtos EOSDIS em geral
são entregues em NetCDF-4/HDF5 (dados raster multidimensionais, sem variáveis
categóricas), incompatíveis com as exigências da ME. O FIRMS é o serviço do
EOSDIS que entrega dados **tabulares** com variáveis numéricas *e* categóricas
na mesma tabela.

## Variáveis analisadas

- **Numérica principal:** `frp` — *Fire Radiative Power* (MW). Escala de razão.
- **Categórica:** `satellite` — `Terra` ou `Aqua`. Escala nominal.
- **Auxiliar (item d):** `daynight` — `D` (diurno) ou `N` (noturno).

> Atenção: no MODIS a coluna `confidence` é **numérica (0–100)**. No VIIRS ela
> seria categórica (`low`/`nominal`/`high`). Isso muda a classificação da escala
> de medida no item (a).

## Pré-requisitos

O CSV bruto precisa existir em `dados/bruto/` (o caminho está em
`config.ARQUIVO_BRUTO`). Sem esse arquivo o pipeline não roda — não há
chamada à API da NASA.

### Instalar as dependências

O projeto usa a `venv` na raiz de `Big_Data`:

```powershell
..\venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Como executar

```powershell
# Valida os cálculos com dados sintéticos (não precisa do CSV real)
..\venv\Scripts\python.exe validar_pipeline.py

# Executa o pipeline real a partir do CSV local
..\venv\Scripts\python.exe main.py
```

Saídas produzidas:

- `dados/bruto/` — CSV original do FIRMS, fonte única da análise
- `dados/processado/focos_tratados.csv` — dataset limpo
- `graficos/*.png` — 4 figuras prontas para o relatório
- `relatorio/resultados.md` — todos os números formatados, com os trechos
  `[ESCREVA AQUI]` indicando onde entra sua argumentação

Guia de escrita (não é gerado pelo script, é material de apoio):

- `relatorio/esqueleto_relatorio.md` — molde do documento final: estrutura das
  seções, perguntas que cada parágrafo deve responder, referências em ABNT já
  prontas e checklist de entrega

## Arquitetura

Cada módulo corresponde a um item avaliado da ME, o que permite rodar e revisar
um item isoladamente:

```
config.py                parâmetros centrais (sensor, país, variáveis, escalas)
main.py                  orquestrador do pipeline
validar_pipeline.py      teste com dados sintéticos, sem depender da API
src/
  coleta.py              (a) CSV local -> DataFrame           [infraestrutura]
  preparacao.py          (a) limpeza e descrição estrutural  [infraestrutura]
  descritiva.py          (b) média, mediana, σ, s², quartis  [domínio]
  probabilidade.py       (d) P(A) e P(A|B)                   [domínio]
  visualizacao.py        (c) gráficos                        [apresentação]
  interpretacao.py       (e) geração do relatório            [apresentação]
```

A camada de **domínio** não importa `matplotlib`: recebe apenas
`Series`/`DataFrame` e devolve números. Essa independência é o que permite
validar os cálculos com dados sintéticos, sem o CSV real.

## Mapa de pontuação

| Item | Módulo responsável | Pontos |
| --- | --- | --- |
| a — Coleta, importação e descrição | `coleta.py`, `preparacao.py` | 0,3 |
| b — Cálculos estatísticos e justificativa | `descritiva.py` | 0,6 |
| c — Visualizações | `visualizacao.py` | 0,4 |
| d — Probabilidade simples e condicional | `probabilidade.py` | 0,3 |
| e — Interpretação, insights e decisões | `interpretacao.py` + redação | 0,4 |
| **Total** | | **2,0** |

## O que ainda depende de você

O código produz as evidências quantitativas; a **argumentação** vale 1,0 ponto
(a justificativa do item b mais o item e inteiro) e precisa ser escrita por
você. Procure os marcadores `[ESCREVA AQUI]` em `relatorio/resultados.md`.
