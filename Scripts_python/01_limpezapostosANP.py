# =============================================
# Script 01 - Limpeza dos dados da ANP
# Projeto: Rede de Postos Autônomos - Vale do Paraíba
# Objetivo: Manter só as colunas úteis e filtrar a região
# =============================================

import pandas as pd

# ================== CONFIGURAÇÃO ==================

# Caminho do arquivo baixado da ANP
arquivo_entrada = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_anp.xlsx"

# Caminho do arquivo limpo que será gerado
arquivo_saida = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_limpo.csv"

# ================== LEITURA DO ARQUIVO ==================

df = pd.read_excel(arquivo_entrada)

# Visualizar as primeiras linhas para conferir
print(df.head())

# Lista dos municípios do Vale do Paraíba (oficial - 39 cidades)
municipios_vale = [
    'APARECIDA', 'ARAPEI', 'AREIAS', 'BANANAL', 'CACAPAVA', 'CACHOEIRA PAULISTA',
    'CAMPOS DO JORDAO', 'CANAS', 'CARAGUATATUBA', 'CRUZEIRO', 'CUNHA', 'GUARATINGUETA',
    'IGARATA', 'ILHABELA', 'JACAREI', 'JAMBEIRO', 'LAGOINHA', 'LAVRINHAS', 'LORENA',
    'MONTEIRO LOBATO', 'NATIVIDADE DA SERRA', 'PARAIBUNA', 'PINDAMONHANGABA',
    'PIQUETE', 'POTIM', 'QUELUZ', 'REDENCAO DA SERRA', 'ROSEIRA','SANTA BRANCA', 'SANTA BRIGIDA',
    'SANTA ISABEL', 'SAO BENTO DO SAPUCAI', 'SAO JOSE DOS CAMPOS', 'SAO LUIS DO PARAITINGA',
    'SÃO SEBASTIAO', 'SILVEIRAS', 'TAUBATE', 'TREMEMBE', 'UBATUBA', 'VARGEM'
]

# Colunas que vamos manter (as mais importantes para nosso case)
colunas_para_manter = [
    'Código', 'CNPJ', 'Razão Social', 'Nome Fantasia', 
    'Endereço', 'Número', 'Bairro', 'CEP', 'Município', 'UF',
    'Bandeira', 'Tipo de Posto', 'Número de Bicos', 
    'Capacidade de Armazenamento (m³)', 'Data de Autorização'
]

print("Iniciando limpeza dos dados da ANP...")

# ================== CARREGAR OS DADOS ==================
# Tenta ler como Excel primeiro, depois como CSV se der erro
try:
    df = pd.read_excel(arquivo_entrada)
except:
    df = pd.read_csv(arquivo_entrada, encoding='utf-8', low_memory=False)

print(f"Arquivo carregado com {len(df)} postos no total.")

# ================== LIMPEZA ==================

# Ajuste para o nome real da coluna no dataset
df['MUNICÍPIO'] = df['MUNICÍPIO'].str.upper().str.strip()

# 1. Manter só as colunas que queremos
# (mantido exatamente como você escreveu)
# df = df[colunas_para_manter]

# 2. Filtrar apenas os municípios do Vale do Paraíba
df = df[df['MUNICÍPIO'].isin(municipios_vale)]

# 3. Limpar espaços extras nos nomes das colunas e textos
df.columns = df.columns.str.strip()
df = df.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

print(f"Após filtro: {len(df)} postos na região do Vale do Paraíba.")

# ================== SALVAR ==================
df.to_csv(arquivo_saida, index=False, encoding='utf-8')

print("✅ Arquivo limpo salvo com sucesso!")
print(f"   → {arquivo_saida}")
print("\nAgora você pode abrir esse CSV no Power BI ou continuar com mais scripts.")