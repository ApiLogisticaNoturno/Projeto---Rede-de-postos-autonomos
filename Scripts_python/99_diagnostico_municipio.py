import pandas as pd

# Caminho do arquivo ORIGINAL da ANP
caminho_arquivo = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_anp.xlsx"

# Carrega o Excel como DataFrame
df_original = pd.read_excel(caminho_arquivo)

# Cidades que queremos procurar
cidades_procuradas = [
    'SAO JOSE DOS CAMPOS',
    'JACAREI',
    'TAUBATE',
    'SAO JOSE',
    'JACAREÍ',
    'TAUBATÉ'
]

print("🔍 Verificando como a ANP escreve as cidades...\n")

for cidade in cidades_procuradas:
    
    encontrados = df_original[
        df_original['MUNICÍPIO']
        .astype(str)
        .str.upper()
        .str.contains(cidade, na=False)
    ]

    if not encontrados.empty:
        nomes_reais = encontrados['MUNICÍPIO'].unique()
        print(f"✅ Encontrados {len(encontrados)} postos em: {nomes_reais.tolist()}")
    else:
        print(f"❌ Nenhuma ocorrência de '{cidade}'")