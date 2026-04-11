# =============================================
# Script 04_v2 - Análise de Demanda - Apenas Vale do Paraíba
# Usa MUNICÍPIO (ANP) e Município (IBGE) + filtro da região
# =============================================

import pandas as pd
from unidecode import unidecode

print("🚀 Iniciando análise de demanda - Foco no Vale do Paraíba...")

# ================== SEUS CAMINHOS ==================
caminho_postos = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_com_coordenadas_completas.csv"
caminho_ibge = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\municipios_sp_populacao_2025.csv"
arquivo_saida = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\analise_demanda_vale_paraiba.csv"

# ================== LISTA OFICIAL DO VALE DO PARAÍBA ==================
municipios_vale = [
    'APARECIDA', 'ARAPEÍ', 'AREIAS', 'BANANAL', 'CAÇAPAVA', 'CACHOEIRA PAULISTA',
    'CAMPOS DO JORDÃO', 'CANAS', 'CARAGUATATUBA', 'CRUZEIRO', 'CUNHA', 'GUARATINGUETÁ',
    'IGARATÁ', 'ILHABELA', 'JACAREI', 'JAMBEIRO', 'LAGOINHA', 'LAVRINHAS', 'LORENA',
    'MONTEIRO LOBATO', 'NATIVIDADE DA SERRA', 'PARAIBUNA', 'PINDAMONHANGABA',
    'PIQUETE', 'POTIM', 'QUELUZ', 'REDENÇÃO DA SERRA', 'ROSEIRA', 'SANTA BRANCA',
    'SANTA ISABEL', 'SÃO BENTO DO SAPUCAÍ', 'SAO JOSE DOS CAMPOS', 'SÃO LUÍS DO PARAITINGA',
    'SÃO SEBASTIÃO', 'SILVEIRAS', 'TAUBATE', 'TREMEMBÉ', 'UBATUBA', 'VARGEM'
]

# ================== FUNÇÃO DE PADRONIZAÇÃO ==================
def padronizar_cidade(cidade):
    if pd.isna(cidade):
        return None
    cidade = unidecode(str(cidade))
    cidade = cidade.upper().strip()
    return cidade

# ================== CARREGAR E FILTRAR ==================
df_postos = pd.read_csv(caminho_postos)
df_postos['Municipio_Padrao'] = df_postos['MUNICÍPIO'].apply(padronizar_cidade)

# Conta postos
postos_por_mun = df_postos['Municipio_Padrao'].value_counts().reset_index()
postos_por_mun.columns = ['Municipio_Padrao', 'Postos_Existentes']

# Carrega IBGE e filtra só o Vale do Paraíba
df_pop = pd.read_csv(caminho_ibge)
df_pop['Municipio_Padrao'] = df_pop['Município'].apply(padronizar_cidade)

# Filtra apenas municípios do Vale
df_pop_vale = df_pop[df_pop['Municipio_Padrao'].isin([padronizar_cidade(m) for m in municipios_vale])]

print(f"Total de municípios do Vale do Paraíba no IBGE: {len(df_pop_vale)}")

# Junção
df_analise = pd.merge(df_pop_vale, postos_por_mun, on='Municipio_Padrao', how='left')
df_analise['Postos_Existentes'] = df_analise['Postos_Existentes'].fillna(0).astype(int)

# Calcula densidade
df_analise['Postos_por_100mil'] = (df_analise['Postos_Existentes'] / df_analise['Populacao_2025'] * 100000).round(2)

# Ordena (menor densidade primeiro)
df_analise = df_analise.drop(columns=['Municipio_Padrao']).sort_values('Postos_por_100mil')

# ================== RESULTADO ==================
print("\n✅ Análise concluída - Apenas Vale do Paraíba!")
print(f"Total de municípios analisados: {len(df_analise)}")
print(f"Total de postos: {df_analise['Postos_Existentes'].sum()}")

print("\n🔥 10 MELHORES OPORTUNIDADES para novos postos autônomos (menor densidade):")
print(df_analise[['Município', 'Populacao_2025', 'Postos_Existentes', 'Postos_por_100mil']].head(10).to_string(index=False))

# Salva
df_analise.to_csv(arquivo_saida, index=False, encoding='utf-8')
print(f"\n📁 Arquivo salvo em: {arquivo_saida}")
print("Agora importe esse arquivo no Power BI para criar a tabela!")