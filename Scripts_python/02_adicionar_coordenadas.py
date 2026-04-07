# =============================================
# Script 02_v3 - Adicionar Latitude e Longitude (versão ajustada para seus dados ANP)
# Projeto: Rede de Postos Autônomos - Vale do Paraíba
# Usa geopy + Nominatim com endereço completo
# =============================================

import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import time

# ================== CONFIGURAÇÃO ==================
#arquivo_entrada = '../dados/postos_vale_paraiba_limpo.csv'
#arquivo_saida = '../dados/postos_vale_paraiba_com_coordenadas.csv'

arquivo_entrada = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_limpo.csv"
arquivo_saida = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_vale_paraiba_com_coordenadas.csv"

# Configura o geolocalizador (nome único para o seu projeto)
geolocator = Nominatim(user_agent="postos_autonomos_vale_paraiba_portfolio")

# Limita velocidade (importante para não bloquear)
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.2)

print("🚀 Iniciando busca de coordenadas com endereço completo...")
print("Isso vai demorar cerca de 4 a 6 minutos para 204 postos...")

# Carregar os dados
df = pd.read_csv(arquivo_entrada)

# Criar colunas novas
df['latitude'] = None
df['longitude'] = None

sucesso = 0
falha = 0

print(f"Processando {len(df)} postos...\n")

for index, row in df.iterrows():
    try:
        # Monta um endereço bem completo e natural (melhor chance de achar)
        endereco_parts = []
        
        if pd.notna(row.get('Endereço')):
            endereco_parts.append(str(row['Endereço']).strip())
        
        if pd.notna(row.get('Número')) and str(row['Número']).strip() not in ['0', 'S/N', '', 'nan']:
            endereco_parts.append(str(row['Número']).strip())
        
        if pd.notna(row.get('COMPLEMENTO')):
            endereco_parts.append(str(row['COMPLEMENTO']).strip())
        
        if pd.notna(row.get('BAIRRO')):
            endereco_parts.append(str(row['BAIRRO']).strip())
        
        if pd.notna(row.get('MUNICÍPIO')):
            endereco_parts.append(str(row['MUNICÍPIO']).strip())
        
        endereco_parts.append("SP")  # Estado
        
        endereco_final = ", ".join(filter(None, endereco_parts))
        
        # Busca a coordenada
        location = geocode(endereco_final)
        
        if location:
            df.at[index, 'latitude'] = location.latitude
            df.at[index, 'longitude'] = location.longitude
            sucesso += 1
            print(f"✅ {index+1:3d} - Encontrado: {endereco_final[:60]}...")
        else:
            falha += 1
            print(f"❌ {index+1:3d} - Não encontrado: {endereco_final[:60]}...")
            
    except Exception as e:
        falha += 1
        print(f"⚠️  {index+1:3d} - Erro: {str(e)[:50]}...")
    
    # Mostra progresso a cada 10 postos
    if (index + 1) % 10 == 0:
        print(f"\n--- Progresso: {index+1}/{len(df)} | Sucesso: {sucesso} | Falhas: {falha} ---\n")

print("\n🎉 Busca finalizada!")
print(f"Coordenadas encontradas: {sucesso} de {len(df)}")
print(f"Sem coordenadas: {falha}")

# Salvar o resultado
df.to_csv(arquivo_saida, index=False, encoding='utf-8')

print(f"\n✅ Arquivo salvo em: {arquivo_saida}")
print("Agora você pode importar esse CSV no Power BI e criar o mapa!")