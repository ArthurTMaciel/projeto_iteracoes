#'=================================================================================================
#' FUNCAO: Transformar RAIS.dta em RAIS.csv + id_lepes
#' 
#' AUTOR: Pedro Borges de Melo Filho
#' 
#' DATA: 19/10/2023
#' 
#' MODIFICACOES:
#'=================================================================================================

# Importando as bibliotecas
from tqdm import tqdm
import pandas as pd

# aplicacao da iteracao dos anos RAIS =============================================================

# baixando base com os codigos dos estados do IBGE
br_states = pd.read_csv('rais/ignore/br-state-codes.csv',nrows = 27, usecols = ['subdivision','idIBGE'])

# Convertendo o DataFrame em um dicionário
br_states_dict = br_states.set_index('subdivision')['idIBGE'].to_dict()

# escrevendo o dicionario invertendo 'chave' vs 'valor'
meu_dicionario_str = {str(valor): chave  for chave, valor in br_states_dict.items()}

# Adicionando uma nova info ao dicionario
meu_dicionario_str["0"] = "0"

# Definindo uma funcao para extrair o codigo do estado a partir do mun_trab
def extrair_codigo_estado(mun_codigo):
    if mun_codigo == 0:
        return 0  # Trate codigos ausentes ou invalidos
    info = str(mun_codigo)[:2]  # Extraia os dois primeiros dígitos (codigo do estado)
    return str(info)


# LOOP para bases da RAIS - Estado ================================================================
# abrindo a base de dados

for estado in tqdm(br_states.subdivision, desc= f"estado da RAIS ano:2021", colour = 'blue'):

    # Pegando as colunas da Rais em questao e
    # criando uma base com o nome das colunas
    colunas = pd.read_csv(
        'rais/ignore/RAIS_VINC_PUB_NORDESTE_21.txt',
        encoding= 'latin-1',
        sep = ';',
        nrows = 10
    ).columns.tolist()

    # base da Rais do estado respectivo. Setando colunas ----
    pd.DataFrame( columns = ['estado'] + colunas ).to_csv(
        f"rais\\ignore\\2021\\RAIS_2021_{estado}.csv",
        sep   = ";",
        index = False,
    )
    
    # funcao de leitura das bases de dados iterando por pedacos
    chunks = pd.read_csv(
        'rais/ignore/RAIS_VINC_PUB_NORDESTE_21.txt',
        chunksize  = 2 * (10**6),
        sep = ';',
        on_bad_lines='skip',
        low_memory=False,
        encoding= 'latin-1',
    )

    for df_rais in tqdm(chunks, f"Progesso dos Chunks"):
        
        # aplicando alteracao para codigo do estado
        df_rais.insert(
            loc    = 0,
            column = 'estado',
            value  = df_rais['Município'].apply(extrair_codigo_estado).map(meu_dicionario_str)
        )

        # separando a base de acordo com o estado e salvando-a em um data.frame
        df_rais.loc[df_rais['estado'] == estado].to_csv(
            f"rais\\ignore\\2021\\RAIS_2021_{estado}.csv",
            sep    = ";",
            index  = False,
            header = False,
            mode   = 'a'
        )

#for ano in anos:
#    caminho = f'{path}\\RAIS_{ano}'
#    os.makedirs(caminho)
#    for estado in br_states.subdivision:
#        caminho_estado = f'{path}\\RAIS_{ano}\\RAIS_{ano}_{estado}'
#        os.makedirs(caminho_estado)
'''
# chunks = pd.read_csv(
#     f'E:\\RAIS_CSV\\desidenticada\\RAIS_{2018}_anonimizado.csv',
# #    chunksize  = 2 * (10**6),
#     nrows= 1e3,
#     sep = ';',
#     on_bad_lines='skip',
#     low_memory=False,
#     skiprows=1
# )

# chunks.municipio

colunas = pd.read_csv(
    f'E:\\RAIS_CSV\\desidenticada\\RAIS_{2018}_anonimizado.csv',
    encoding= 'ISO-8859-1',
    sep = ';',
    nrows = 10,
    skiprows=1
    ).columns.tolist()'''