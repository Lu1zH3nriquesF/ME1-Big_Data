# Esqueleto do Relatório Final — ME Big Data (Unidade I)

**Como usar este arquivo:** ele é o *molde* do documento que vocês vão entregar
no Google Docs. Cada seção traz (1) o objetivo dela, (2) de onde vêm os números
e (3) as perguntas que o texto precisa responder. Copie a estrutura para o Docs,
cole as evidências geradas em `resultados.md` e escreva as respostas.

**Não confunda os dois arquivos:**

- `resultados.md` — gerado automaticamente pelo `main.py`. Contém os números,
  tabelas e caminhos dos gráficos. É a sua matéria-prima.
- `esqueleto_relatorio.md` (este) — o roteiro de escrita. Não contém números.

**Distribuição de esforço.** Dos 2,0 pontos, cerca de **1,0 depende de texto
argumentativo** (a justificativa do item b e o item e inteiro). Os outros 1,0
dependem de execução correta, que o código já entrega. Priorize a escrita.

---

## CAPA

Sem numeração. Elementos:

- Nome da instituição e do curso (Análise e Desenvolvimento de Sistemas)
- Disciplina: **Big Data** — Docente: **Luiz Gomes da Cunha Neto**
- Título sugerido: *Análise Estatística de Focos de Calor no Brasil a partir de
  Dados de Sensoriamento Remoto da NASA (FIRMS/EOSDIS)*
- Nome completo e matrícula de **todos os integrantes do grupo**
- Cidade e ano (2026)

> Confirme com o professor o número de integrantes por grupo — o enunciado não
> especifica, e a capa é onde essa informação fica registrada.

---

## 1. INTRODUÇÃO *(1 a 2 parágrafos, sem pontuação direta)*

Não vale nota isoladamente, mas define se o avaliador entende o trabalho já na
primeira página. Não pule.

**Perguntas que o texto deve responder:**

1. Qual é o problema do mundo real? (queimadas no Brasil: impacto ambiental,
   econômico e de saúde pública)
2. Por que dados de satélite são a forma adequada de observar esse problema em
   escala nacional?
3. Qual é o objetivo declarado deste trabalho? (simular um ciclo completo de
   análise de dados, da coleta ao insight, em Python)
4. Qual é a **pergunta de pesquisa** que a análise vai responder?

**Sugestão de pergunta de pesquisa** — escolha uma e mantenha coerência com ela
até a conclusão:

> *Como se distribui a intensidade dos focos de calor detectados no Brasil, e
> existe associação entre a intensidade do fogo e o período (diurno/noturno) em
> que ele é detectado?*

Fechar a introdução declarando a pergunta é o que amarra os itens (d) e (e) ao
resto do relatório, em vez de deixá-los parecendo cálculos soltos.

---

## 2. MATERIAL E MÉTODO *(meia página)*

Atende à exigência "MATERIAL A SER UTILIZADO" do enunciado.

**Conteúdo obrigatório:**

- Linguagem: Python 3.14
- Bibliotecas: `pandas` (manipulação), `numpy` (cálculo numérico),
  `matplotlib` e `seaborn` (visualização)
- Ambiente de desenvolvimento utilizado
- Forma de acesso aos dados: **CSV local** originado do FIRMS, lido pelo
  `pandas` a partir de `dados/bruto/` — o pipeline não faz requisição HTTP

**Parágrafo de justificativa metodológica** (diferencial: mostra leitura crítica
da documentação da fonte):

> Explique por que, dentro do EOSDIS, foi escolhido o FIRMS e não um produto
> raster convencional. Os argumentos: os produtos EOSDIS são majoritariamente
> distribuídos em NetCDF-4/HDF5, formatos de dados matriciais multidimensionais
> que não possuem variáveis categóricas e exigem bibliotecas específicas
> (`xarray`, `h5py`); o FIRMS entrega dados **vetoriais tabulares** em CSV, com
> variáveis quantitativas e qualitativas na mesma tabela, compatíveis com a
> análise exigida.

**Limitação a declarar** (a documentação da NASA alerta explicitamente sobre
isso — citá-la conta a seu favor):

> O produto MCD14DL utilizado é *near real-time* (NRT). O guia oficial do
> usuário recomenda que dados NRT **não** sejam empregados em análises de séries
> temporais longas ou estudos de tendência, para os quais o produto padrão
> MCD14ML é mais apropriado. Como esta análise é um **retrato transversal de
> poucos dias**, e não um estudo de tendência histórica, o uso do NRT é adequado ao
> escopo.

---

## 3. ITEM (a) — DESCRIÇÃO E IMPORTAÇÃO DOS DADOS *(0,3 ponto)*

**Fonte:** seção "Item (a)" de `resultados.md`.

### 3.1 Identificação da fonte

Cole a lista de identificação (órgão, arquivo local, sensor, recorte espacial e
temporal, tema). O enunciado pede "a fonte exata (link direto, nome do
arquivo)" — informe também o nome do CSV salvo em `dados/bruto/`.

### 3.2 Importação e pré-processamento

Cole o código de `coleta.py` (função `coletar_focos`) e de `preparacao.py`
(função `preparar`). Cole a tabela do log de limpeza.

**Perguntas que o texto deve responder:**

1. Por que registros com FRP ausente foram removidos, em vez de preenchidos com
   a média? (a variável é o objeto central da análise; imputar valor inventaria
   intensidade de fogo inexistente)
2. Por que registros com FRP igual a zero foram removidos? (indicam detecção sem
   energia radiativa mensurável e deslocariam a média para baixo)
3. Qual percentual da amostra original foi retido? Esse descarte compromete a
   representatividade?

### 3.3 Características estatísticas das variáveis

Cole a tabela de estrutura (`dtype`, escala de medida, completude).

**Ponto de atenção que rende nota:** explique que no MODIS a coluna `confidence`
é **quantitativa** (0 a 100), enquanto no sensor VIIRS a mesma coluna é
**qualitativa ordinal** (`low`/`nominal`/`high`). Demonstra que vocês leram a
documentação do produto, e não apenas abriram o CSV.

Declare explicitamente o **tamanho da amostra** (nº de linhas x nº de colunas) e
confirme que supera o mínimo de 100 registros exigido.

---

## 4. ITEM (b) — ESTATÍSTICA DESCRITIVA APROFUNDADA *(0,6 ponto)*

O item de maior peso. **Fonte:** seção "Item (b)" de `resultados.md`.

### 4.1 Definição das variáveis analisadas

- **Numérica principal:** `frp` (*Fire Radiative Power*, MW) — escala de razão
- **Categórica:** `satellite` (Terra / Aqua) — escala nominal

Justifique a escolha do FRP em uma frase: é a variável que mede a **intensidade
energética** do fogo, e não apenas sua ocorrência.

### 4.2 Medidas calculadas

Cole as quatro tabelas (tendência central, dispersão, posição, moda) **e o
código** que as gerou (`descritiva.py`). O enunciado exige explicitamente
"o código Python de todos os cálculos e os valores resultantes".

Confira que todas as medidas pedidas estão presentes: média, mediana, desvio
padrão, variância, percentil 75, Q1, Q2, Q3 e a moda da categórica.

### 4.3 Justificativa: média versus mediana *(o texto mais importante do item)*

Cole as tabelas de assimetria e de outliers como evidência.

**Perguntas que o texto deve responder, uma por parágrafo:**

1. **Por que a média é maior que a mediana neste conjunto?** Encadeie o
   raciocínio: a média incorpora todos os valores e por isso é arrastada pelos
   focos extremos; a mediana é posicional e ignora a magnitude das caudas. Cite
   o coeficiente de assimetria calculado e a quantidade de outliers.
2. **O que o desvio padrão representa concretamente aqui?** Não defina o
   conceito — interprete o número. Se o desvio padrão supera a média (coeficiente
   de variação acima de 100%), a conclusão é que a intensidade dos focos é
   extremamente heterogênea: não existe um "foco típico" bem definido.
3. **Qual medida vocês usariam para reportar a intensidade típica, e por quê?**
   Defenda a mediana como medida robusta, e explique em que situação a média
   ainda é útil (por exemplo, para estimar energia total liberada, onde a
   magnitude dos extremos importa).

### 4.4 Comparação entre categorias

Cole a tabela de resumo por satélite. Observe se um satélite detecta focos
sistematicamente mais intensos e **levante a hipótese** do motivo (Terra e Aqua
têm horários de passagem diferentes, o que altera a chance de captar o pico
diário de queimada).

Cuidado com a redação: apresente isso como hipótese a investigar, não como
conclusão provada. Rigor na formulação é bem avaliado.

---

## 5. ITEM (c) — VISUALIZAÇÃO E ANÁLISE DA DISTRIBUIÇÃO *(0,4 ponto)*

**Fonte:** os 4 PNGs em `graficos/`.

Insira cada imagem com legenda numerada (Figura 1, Figura 2...) e cole o código
de `visualizacao.py`.

**O que escrever sobre cada figura** — uma análise por gráfico, não uma legenda:

- **Figura 1 (box plot + histograma):** descreva a **forma** da distribuição.
  Onde está a concentração? A cauda é longa para qual lado? Onde caem os
  quartis em relação à média? Confirme visualmente a assimetria que o número já
  indicou no item (b).
- **Figura 2 (barras por satélite):** qual é a moda e qual o equilíbrio entre as
  categorias? A diferença é relevante ou as categorias são equilibradas?
- **Figura 3 (box plots comparativos):** as duas distribuições se sobrepõem ou
  há deslocamento claro entre elas?
- **Figura 4 (dispersão geográfica):** há concentração regional? Isso é
  compatível com o conhecimento prévio sobre bioma e sazonalidade brasileiros?

**Justifique duas decisões técnicas de visualização** (mostra domínio, não só
uso da biblioteca):

1. Por que o eixo do FRP está em **escala logarítmica**? (em escala linear, os
   poucos focos extremos comprimem toda a massa de dados contra a esquerda e o
   gráfico perde poder informativo)
2. Por que **barras** e não gráfico de pizza? (comparar comprimentos é
   perceptualmente mais preciso que comparar ângulos)

---

## 6. ITEM (d) — PROBABILIDADE SIMPLES E CONDICIONAL *(0,3 ponto)*

**Fonte:** seção "Item (d)" de `resultados.md`. Cole o código de
`probabilidade.py`.

### 6.1 Definição formal dos eventos

Enuncie os eventos antes de calcular. Sem isso, os números não significam nada:

- **A** = a detecção ocorreu no período noturno (`daynight` = `N`)
- **B** = o foco possui FRP acima da média da amostra

### 6.2 Probabilidade simples — P(A)

Cole a tabela. **Perguntas a responder:**

1. Qual o valor de corte (percentil 75) em MW?
2. O resultado ficou próximo do teórico de 0,25? Por quê o valor empírico pode
   divergir levemente? (valores repetidos exatamente no ponto de corte deslocam
   a proporção)

### 6.3 Probabilidade condicional — P(A|B)

Cole a tabela. **Perguntas a responder:**

1. Explique com suas palavras que condicionar em B **reduz o espaço amostral**:
   deixamos de olhar todos os focos e passamos a olhar apenas o subconjunto em
   que B é verdadeiro. Informe o tamanho desse subconjunto reduzido.
2. Compare P(A|B) com P(A). Se forem praticamente iguais, os eventos são
   **independentes** — saber que o fogo é intenso não informa nada sobre o
   período de detecção. Se diferirem, há **dependência**, e vocês devem indicar
   a direção e a magnitude em pontos percentuais.
3. Traduza o resultado em linguagem de negócio: o que isso significa para quem
   opera o combate a incêndios?

> Atenção: independência estatística é um resultado **legítimo e reportável**.
> Se P(A|B) ≈ P(A), não force uma conclusão de associação — afirme a
> independência e explique o que ela implica. Honestidade analítica vale mais
> que um achado inventado.

---

## 7. ITEM (e) — INTERPRETAÇÃO, INSIGHTS E DECISÃO *(0,4 ponto)*

Nenhuma linha de código aqui. É texto do início ao fim.
**Fonte:** a lista "Evidências quantitativas" em `resultados.md`.

### 7.1 Síntese interpretativa

Um ou dois parágrafos costurando os itens (b), (c) e (d) em uma narrativa única.
Volte à pergunta de pesquisa da introdução e responda-a diretamente.

### 7.2 Os três insights de alto valor

O enunciado exige **no mínimo três**. Um insight não é um número repetido — é
uma afirmação sobre o mundo, sustentada por um número.

Estrutura recomendada para cada um:

> **Insight N — [título curto e afirmativo]**
> *Evidência:* [o número ou gráfico que sustenta]
> *Interpretação:* [o que isso significa no mundo real]
> *Relevância:* [por que alguém deveria se importar]

Direções sugeridas (desenvolva com os seus números):

1. **Concentração da intensidade** — a distribuição fortemente assimétrica
   indica que uma minoria de focos responde pela maior parte da energia
   liberada. Implicação: estratégias uniformes de combate são ineficientes.
2. **Padrão temporal de detecção** — o resultado da probabilidade condicional
   informa se focos intensos se concentram em algum período. Implicação direta
   sobre turnos e janelas de monitoramento.
3. **Concentração geográfica** — a dispersão espacial revela regiões críticas.
   Implicação sobre onde posicionar recursos fisicamente.

### 7.3 Decisões organizacionais propostas

O enunciado pede decisões que "uma organização (governo, empresa, ONG)" poderia
tomar "utilizando os resultados como evidência". Nomeie a organização.

**Regra de ouro: cada decisão deve citar o número que a justifica.** Uma decisão
sem evidência numérica é opinião, e é exatamente aí que se perde ponto.

Direções, para desenvolver:

- **Limiar automático de alerta:** adotar o percentil 75 do FRP (valor concreto
  em MW, extraído da análise) como gatilho de acionamento prioritário de
  brigada. Justificativa: concentra recursos nos 25% de focos mais energéticos.
- **Dimensionamento de turnos:** ajustar a escala de plantão conforme o padrão
  diurno/noturno medido no item (d).
- **Alocação territorial:** priorizar as regiões de maior densidade de focos
  identificadas na Figura 4.
- **Política de dados:** manter o CSV bruto versionado junto do código, para
  que a análise seja reproduzível sem depender da disponibilidade da API FIRMS.

---

## 8. CONCLUSÃO *(1 parágrafo)*

Retome o objetivo, responda à pergunta de pesquisa em uma frase, cite o
resultado mais relevante e aponte uma limitação e um próximo passo.

**Limitações honestas a mencionar** (declarar limitação demonstra maturidade
analítica, não fraqueza):

- Janela temporal curta (recorte de poucos dias no CSV): não permite conclusões sazonais
- Dados NRT sujeitos a reprocessamento posterior pelo produto MCD14ML
- Detecção por satélite tem viés de cobertura: nuvens e horários de passagem
  podem ocultar focos reais
- Correlações observadas não estabelecem causalidade

---

## REFERÊNCIAS

Prontas para uso — confira o formato exigido pela sua instituição e **substitua
a data de acesso** pela data real da coleta.

**Conjunto de dados (referência principal):**

> NASA. **MODIS/Aqua+Terra Thermal Anomalies/Fire locations 1km FIRMS V0061 NRT
> (MCD14DL)**. NASA Land, Atmosphere Near real-time Capability for EOS (LANCE) /
> Fire Information for Resource Management System (FIRMS), 2026.
> DOI: 10.5067/FIRMS/MODIS/MCD14DL.NRT.0061. Disponível em:
> https://firms.modaps.eosdis.nasa.gov/. Acesso em: __ set. 2026.

**Artigo do algoritmo de detecção (cite ao explicar como o FRP é obtido):**

> GIGLIO, L.; SCHROEDER, W.; JUSTICE, C. O. The collection 6 MODIS active fire
> detection algorithm and fire products. **Remote Sensing of Environment**,
> v. 178, p. 31-41, 2016. DOI: 10.1016/j.rse.2016.02.054.

**Artigo do próprio sistema FIRMS:**

> DAVIES, D. K.; ILAVAJHALA, S.; WONG, M. M.; JUSTICE, C. O. Fire Information
> for Resource Management System: Archiving and Distributing MODIS Active Fire
> Data. **IEEE Transactions on Geoscience and Remote Sensing**, v. 47, n. 1,
> p. 72-79, 2009. DOI: 10.1109/TGRS.2008.2002076.

**Guia do usuário (cite ao declarar a limitação do NRT):**

> NASA. **MODIS Collection 6/6.1 Active Fire Product User's Guide**. NASA
> Earthdata, 2023. Disponível em: https://www.earthdata.nasa.gov/. Acesso em:
> __ set. 2026.

> Inclua também as referências das UAs do catálogo Sagah listadas no enunciado
> (Ciência de Dados e Big Data; Inferência Estatística; etc.), conforme o
> professor solicitar.

---

## APÊNDICE — CÓDIGO-FONTE

O enunciado exige que o código seja "anexado ou ter seu link compartilhado no
relatório". Escolha uma opção:

- **Repositório GitHub** (recomendado se o grupo for colaborar): link público
- **Google Colab**: link de compartilhamento com permissão de leitura
- **Anexo**: os arquivos `.py` em anexo ao PDF

Inclua também a árvore de diretórios do projeto e a instrução de execução
(`python main.py`), para que o professor consiga reproduzir a análise.

O CSV em `dados/bruto/` é a fonte da análise e deve acompanhar o código.

---

## CHECKLIST FINAL ANTES DE ENTREGAR

- [ ] Todos os `[ESCREVA AQUI]` de `resultados.md` foram substituídos por texto
- [ ] Média, mediana, desvio padrão, variância, percentil 75, Q1, Q2, Q3 e moda
      estão todos presentes e visíveis (checagem literal do enunciado)
- [ ] No mínimo 2 gráficos, com os quartis destacados em um deles
- [ ] P(A) e P(A|B) calculadas, com os eventos formalmente enunciados
- [ ] No mínimo 3 insights, cada um com evidência numérica
- [ ] Decisões organizacionais propostas, cada uma citando um número
- [ ] Amostra com mais de 100 registros, declarada explicitamente
- [ ] Código Python visível no corpo do relatório (não apenas no anexo)
- [ ] Link do código funcionando e acessível a quem não é do grupo
- [ ] Nomes e matrículas de todos os integrantes na capa
- [ ] Data de acesso preenchida nas referências
- [ ] Entrega em Google Docs ou PDF
