import pandas as pd
from unidecode import unidecode

# caminhos
caminho_ibge = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\municipios_sp_populacao_2025.csv"
caminho_anp = r"C:\Users\CARLIN\OneDrive\Área de Trabalho\Projetos Python\Postos_Autonomos\Dados\postos_anp.xlsx"

# carregar arquivos
ibge = pd.read_csv(caminho_ibge)
anp = pd.read_excel(caminho_anp)

# função de padronização
def padronizar_cidade(cidade):
    if pd.isna(cidade):
        return cidade
    cidade = unidecode(str(cidade))
    cidade = cidade.upper().strip()
    return cidade

# criar colunas padronizadas
ibge["cidade_padrao"] = ibge["Município"].apply(padronizar_cidade)
anp["cidade_padrao"] = anp["MUNICÍPIO"].apply(padronizar_cidade)

# comparar cidades após padronização
cidades_ibge = set(ibge["cidade_padrao"].unique())
cidades_anp = set(anp["cidade_padrao"].unique())

nao_encontradas = cidades_anp - cidades_ibge

print("\nQuantidade cidades IBGE:", len(cidades_ibge))
print("Quantidade cidades ANP:", len(cidades_anp))

print("\nCidades da ANP que ainda não batem:")
print(sorted(list(nao_encontradas))[:20])