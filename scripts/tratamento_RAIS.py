# =================================================================================================
# PROJETO: THP - Santa Luzia do Itahy
#
# OBJETIVO: Capturar dados da RAIS para analise
#
# AUTOR: Pedro Borges de Melo Filho
#
# DATA: 10/06/2024
# =================================================================================================
# Importando dependencias
import pandas as pd
import os
import re
import py7zr

# Setando variaveis de diretorio ==================================================================
# Diretórios (substitua pelos seus caminhos)
diretorio_origem = r"E:\\RAIS_nova\\RAIS"
diretorio_destino = r"D:\\Projeto_impacto_tmallkj"

# Expressão regular para UFs do Nordeste
regex_ufs_nordeste = re.compile(r"^(AL|BA|CE|MA|PB|PE|PI|RN|SE)")

for ano in range(2012, 2022):
    # Diretório do ano em questão
    diret_ano = os.path.join(diretorio_origem, str(ano))

    # Iterar sobre os arquivos da pasta do ano
    for nome_arquivo in os.listdir(diret_ano):
        # Verificar se o arquivo começa com uma UF do Nordeste e termina com ".7z"
        if regex_ufs_nordeste.match(nome_arquivo) and nome_arquivo.endswith(".7z"):
            caminho_arquivo_7z = os.path.join(diret_ano, nome_arquivo)
            
            # Descompactar o arquivo usando py7zr
            try:
                with py7zr.SevenZipFile(caminho_arquivo_7z, mode='r') as z:
                    z.extractall(path=os.path.join(diretorio_destino, str(ano)))
                print(f"descompactou pasta de caminho: {caminho_arquivo_7z}")
            except Exception as e:
                print(f"Erro ao descompactar {caminho_arquivo_7z}: {e}")





# filtrando os dados para pegar apenas os municipios de recorte

# tentativa de leitura de uma das bases e tranformacao em um conjunto de csv
teste = pd.read_csv("RAIS/2012/AL2012.txt",sep=";",encoding='latin1', low_memory=False)

pd.unique(teste["Município"]) 

teste.columns
# Filtrar colunas relevantes e vínculos ativos
df_filtrado = teste[['Vl Remun Média Nom', 'Município', 'Vínculo Ativo 31/12']]
df_vinculo_ativo = df_filtrado[df_filtrado['Vínculo Ativo 31/12'] == 1]

# corrigindo coluna de valores
df_filtrado['Vl Remun Média Nom'] = df_filtrado['Vl Remun Média Nom'].str.replace(',','.').astype(float)

# Agrupando por municipio, calcular media da renda e contar contratos
agregacao = df_filtrado.groupby('Município').agg(
    media_remuniracao=('Vl Remun Média Nom', 'mean'),
    numero_contratos=('Vl Remun Média Nom', 'count')
).reset_index()

