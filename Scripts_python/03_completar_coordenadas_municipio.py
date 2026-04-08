# =============================================
# Script 03 - Completar coordenadas faltantes por município
# Projeto: Rede de Postos Autônomos - Vale do Paraíba
# Objetivo: Preencher os 104 postos sem coordenada usando o centro do município
# =============================================

import pandas as pd

# ================== CONFIGURAÇÃO ==================
#arquivo_entrada = '../dados/postos_vale_paraiba_com_coordenadas.csv'
#arquivo_saida = '../dados/postos_vale_paraiba_com_coordenadas_completas.csv'

arquivo_entrada = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_com_coordenadas.csv"
arquivo_saida = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_com_coordenadas_completas.csv"




print("Iniciando preenchimento das coordenadas faltantes por município...")

# Carregar os dados (com as 100 coordenadas já encontradas)
df = pd.read_csv(arquivo_entrada)

# Dicionário com coordenadas aproximadas do centro de cada município do Vale do Paraíba
# (valores reais e confiáveis)
coordenadas_municipio = {
    'APARECIDA': (-22.8514, -45.2347),
    'ARAPEÍ': (-22.6719, -44.9453),
    'AREIAS': (-22.5803, -44.7006),
    'BANANAL': (-22.6825, -44.3231),
    'CAÇAPAVA': (-23.0992, -45.7078),
    'CACHOEIRA PAULISTA': (-22.6653, -45.0128),
    'CAMPOS DO JORDÃO': (-22.7394, -45.5914),
    'CANAS': (-22.7272, -45.0522),
    'CARAGUATATUBA': (-23.6203, -45.4128),
    'CRUZEIRO': (-22.5719, -44.9642),
    'CUNHA': (-23.0747, -44.9600),
    'GUARATINGUETÁ': (-22.8164, -45.1925),
    'IGARATÁ': (-23.2047, -46.0000),
    'ILHABELA': (-23.7781, -45.3581),
    'JACAREÍ': (-23.3053, -45.9658),
    'JAMBEIRO': (-23.2536, -45.6889),
    'LAGOINHA': (-22.9375, -45.1931),
    'LAVRINHAS': (-22.5708, -44.8917),
    'LORENA': (-22.7308, -45.1247),
    'MONTEIRO LOBATO': (-22.9553, -45.8397),
    'NATIVIDADE DA SERRA': (-23.3778, -45.2639),
    'PARAIBUNA': (-23.3869, -45.6625),
    'PINDAMONHANGABA': (-22.9239, -45.4617),
    'PIQUETE': (-22.6033, -45.1761),
    'POTIM': (-22.8517, -45.2542),
    'QUELUZ': (-22.5364, -44.7778),
    'REDENÇÃO DA SERRA': (-23.2669, -45.5369),
    'ROSEIRA': (-22.8986, -45.3069),
    'SANTA BRÍGIDA': (-22.7539, -45.1217),   # ajuste se necessário
    'SANTA ISABEL': (-23.3153, -46.2214),
    'SÃO BENTO DO SAPUCAÍ': (-22.6889, -45.7397),
    'SÃO JOSÉ DOS CAMPOS': (-23.1791, -45.8872),
    'SÃO LUÍS DO PARAITINGA': (-23.2219, -45.3106),
    'SÃO SEBASTIÃO': (-23.7600, -45.4097),
    'SILVEIRAS': (-22.6639, -44.8522),
    'TAUBATÉ': (-23.0264, -45.5556),
    'TREMEMBÉ': (-22.9583, -45.5464),
    'UBATUBA': (-23.4331, -45.0711),
    'VARGEM': (-22.8917, -46.1833)
}

# Contadores
preenchidos = 0

# Preencher apenas os que estão vazios
for index, row in df.iterrows():
    if pd.isna(row['latitude']) or pd.isna(row['longitude']):
        mun = str(row['MUNICÍPIO']).strip().upper()
        if mun in coordenadas_municipio:
            lat, lon = coordenadas_municipio[mun]
            df.at[index, 'latitude'] = lat
            df.at[index, 'longitude'] = lon
            preenchidos += 1

print(f"✅ Preenchidos {preenchidos} postos com coordenadas aproximadas do município.")
print(f"Total com coordenadas agora: {len(df) - df['latitude'].isna().sum()} de {len(df)}")

# Salvar o arquivo final
df.to_csv(arquivo_saida, index=False, encoding='utf-8')

print(f"\nArquivo completo salvo em: {arquivo_saida}")
print("Agora está pronto para o Power BI!")