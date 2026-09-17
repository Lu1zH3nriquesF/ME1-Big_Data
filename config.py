"""Parâmetros centrais do projeto: única fonte de verdade para configuração.

Concentrar as constantes aqui evita "números mágicos" espalhados pelos módulos.
Para mudar de sensor, país ou variável analisada, altere apenas este arquivo.
"""
from pathlib import Path

# --------------------------------------------------------------------------
# Diretórios (resolvidos a partir da raiz do projeto, nunca do cwd, para que
# o pipeline funcione mesmo se executado de outra pasta)
# --------------------------------------------------------------------------
RAIZ = Path(__file__).resolve().parent
DIR_DADOS_BRUTO = RAIZ / "dados" / "bruto"
DIR_DADOS_PROCESSADO = RAIZ / "dados" / "processado"
DIR_GRAFICOS = RAIZ / "graficos"
DIR_RELATORIO = RAIZ / "relatorio"

# --------------------------------------------------------------------------
# Fonte local (CSV originado do NASA FIRMS / EOSDIS)
# --------------------------------------------------------------------------
# O pipeline NÃO faz requisição HTTP. A origem intelectual dos dados continua
# sendo o FIRMS; o meio de obtenção é o arquivo abaixo, já persistido em disco.
PORTAL_FIRMS = "https://firms.modaps.eosdis.nasa.gov/"

# MODIS_NRT = near real-time; metadado da extração original, usado no relatório.
SENSOR = "MODIS_NRT"

# Código ISO de 3 letras do recorte espacial da extração original.
PAIS = "BRA"

# Única fonte de dados em tempo de execução. Troque o nome se substituir o CSV.
ARQUIVO_BRUTO = DIR_DADOS_BRUTO / "firms_MODIS_NRT_BRA_20260911_211449.csv"

# --------------------------------------------------------------------------
# Variáveis da análise estatística (itens b, c e d da ME)
# --------------------------------------------------------------------------

# FRP (Fire Radiative Power, em megawatts) mede a intensidade radiativa do
# foco de calor. Escolhida como variável principal porque tem distribuição
# fortemente assimétrica à direita, o que torna a comparação entre média e
# mediana (exigida no item b) estatisticamente significativa.
VARIAVEL_NUMERICA = "frp"
ROTULO_NUMERICA = "FRP - Potência Radiativa do Fogo (MW)"

# No MODIS, 'satellite' assume os valores 'Terra' e 'Aqua' (satélites que
# carregam o sensor). É uma variável qualitativa NOMINAL, adequada para moda.
# Atenção: no MODIS a coluna 'confidence' é NUMÉRICA (0-100), diferente do
# VIIRS, onde é categórica (low/nominal/high).
VARIAVEL_CATEGORICA = "satellite"
ROTULO_CATEGORICA = "Satélite de Detecção"

# Percentil usado no item d para definir o evento da probabilidade simples.
PERCENTIL_ALVO = 0.75

# Colunas mínimas que o CSV do FIRMS deve conter para a análise ser possível.
COLUNAS_OBRIGATORIAS = (
    "latitude",
    "longitude",
    "brightness",
    "acq_date",
    "acq_time",
    "satellite",
    "confidence",
    "frp",
    "daynight",
)

# --------------------------------------------------------------------------
# Escala de medida de cada variável (item a da ME)
# --------------------------------------------------------------------------
# Mapeamento declarativo usado para documentar a natureza estatística das
# colunas no relatório. Sem isso, a "escala de medida" teria de ser escrita
# manualmente a cada execução.
ESCALAS_DE_MEDIDA = {
    "latitude": "Intervalar (o zero (Equador) é arbitrário, não indica ausência)",
    "longitude": "Intervalar (o zero (Greenwich) é convencional)",
    "brightness": "De razão (temperatura em Kelvin possui zero absoluto)",
    "bright_t31": "De razão (temperatura em Kelvin possui zero absoluto)",
    "scan": "De razão (tamanho do pixel, zero significa ausência)",
    "track": "De razão (tamanho do pixel, zero significa ausência)",
    "acq_date": "Intervalar (data: diferenças fazem sentido, razões não)",
    "acq_time": "Intervalar (hora do dia em formato HHMM)",
    "satellite": "Nominal (Terra / Aqua, sem ordem natural)",
    "instrument": "Nominal (identificação do sensor)",
    "confidence": "De razão (percentual de 0 a 100 de confiança na detecção)",
    "version": "Nominal (identificador da versão do algoritmo)",
    "frp": "De razão (potência em MW, zero significa ausência de energia)",
    "daynight": "Nominal dicotômica (D = diurno, N = noturno)",
    "type": "Nominal (categoria da fonte térmica detectada)",
    "country_id": "Nominal (código do país)",
    # Coluna derivada, criada na etapa de preparação a partir de acq_date + acq_time.
    "data_hora": "Intervalar (timestamp da detecção)",
}
