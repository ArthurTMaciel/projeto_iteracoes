# =================================================================================================
# PROJETO: THP - Santa Luzia do Itanhy
#
# OBJETIVO: Capturar dados para formar grupos de comparacao com Itanhy
#
# AUTOR: Pedro Borges de Melo Filho
#
# DATA: 10/06/2024
# =================================================================================================
# Importando dependencias
import pandas as pd

# importando as bases de dados ====================================================================

# Demografia -------------------------------
# info de dados demograficos dos municipios
demogr = pd.read_csv("Informacoes_grupos/Demografia/dadosDemograficos.csv", sep=';')
# informacoes de prop de negros e pardos por municipio
baseProp = pd.read_csv("Informacoes_grupos/Demografia/prop_pretosPardos_muni.csv", sep=';')

# Saude ------------------------------------
# dados de idh por municipio
idh = pd.read_csv("Informacoes_grupos/Saude/ipeadata_IDH.csv",sep=';')
# dados de idh por municipio
espVida = pd.read_csv("Informacoes_grupos/Saude/esperancaVida.csv",sep=';')

# Emprego e Renda --------------------------
# info de desemprego
txDesemp = pd.read_csv("Informacoes_grupos/Emprego_Renda/taxaDesemprego2.csv", sep=';')
# renda percapta
perCapta = pd.read_csv("Informacoes_grupos/Emprego_Renda/rendaPerCapita.csv")

# Educacionais -----------------------------
# expectativa de Anos de Estudo
expEstudo = pd.read_csv('Informacoes_grupos/Educacionais/expectativaAnosEstudo.csv', sep=';')
# taxa de analfabetismo
txAnalf = pd.read_csv('Informacoes_grupos/Educacionais/taxaAnalfabetismo.csv', sep=';') 

# tratamento inicial das base de dados ============================================================

# # Corrigindo mal identificacao das colunas
# muni = baseProp['municipio'][0] # def a primeira var para iteracao 
# for i in range(len(baseProp)):
#     if  baseProp['municipio'][i] == 'nan':
#         baseProp.loc[i,'municipio'] = muni # atribuindo o resultado
#         baseProp.loc[i,'codigo']  = codigo # atribuindo o resultado
# 
#     codigo = baseProp['codigo'][i]
#     muni   = baseProp['municipio'][i]
# 


# base de prop_raca -----------------------------------------------------------

# # filtros iniciais
# dmgr = dmgr.loc[ dmgr['domicilio'] == 'Total' ,['codigo', 'municipio', 'numeroPessoas'] ]
# 
# # mudando o tipo da variavel para integer
# dmgr['codigo'] = dmgr['codigo'].astype(int)
# 
# # criando uma coluna de estados
# dmgr['Sigla'] = dmgr['municipio'].astype(str).str[-3:-1]
# 
# # corrigindo coluna de municipios
# dmgr['municipio'] = dmgr['municipio'].str[:-5]
# 
# dmgr.to_csv('Informacoes_grupos/Demografia/dadosDemograficos.csv',sep=';', index=False)

# capturando os IDHs que sao proximos do de Santa Luzia ===========================================
  
# corrigindo a virgula nos dados de IDH
idh['IDH'] = idh['IDH'].astype(float)

# Ordenando dataframe por nota de IDH
idh.sort_values(by= "IDH", inplace=True)

# Resetando o index como sendo de 0 ate o numero de linhas do data.frame
idh.reset_index(drop=True, inplace=True)

# pegando a posicao do index onde estah Santa Luzia
indexRankSantaLuzia = idh[idh['municipio'] == 'Santa Luzia do Itanhy'].index.tolist()[0]

# selecionando as faixas baseado em porcentagem
quadranteSantaLuzia = round( (indexRankSantaLuzia / len(idh)), 4)

# definindo a porcentagem de corte
pct_de_corte = 0.005 # valor = 0,5%

# menor e maior valores de corte
maiorCorte = round( (quadranteSantaLuzia + pct_de_corte) * len(idh) )
menorCorte = round( (quadranteSantaLuzia - pct_de_corte) * len(idh) )

# lista dos valores de corte
lista_IDH_parecidos = [int(i) for i in range ( menorCorte, maiorCorte + 1 )]

# numero de municipios selecionados
n_selecionados = len(lista_IDH_parecidos)

# lista de municipios agrupados por IDH
idh_agrupada = idh.loc[lista_IDH_parecidos]

# Capturando municipios com Prop de Pretos proxima a cidade alvo ==================================

# filtrando apenas aqueles de cor 'Preta'
baseProp = baseProp[(baseProp['cor'] == 'Preta')]

# Ordenando dataframe por nota de IDH
baseProp.sort_values(by= "valor_pct", inplace=True)

# Resetando o index como sendo de 0 ate o numero de linhas do data.frame
baseProp.reset_index(drop=True, inplace=True)

# pegando a posicao do index onde estah Santa Luzia
indexPretosSantaLuzia = baseProp[baseProp['municipio'] == 'Santa Luzia do Itanhy'].index.tolist()[0]

# selecionando as faixas baseado em porcentagem
quadranteSantaLuzia = round( (indexPretosSantaLuzia / len(baseProp)), 4)

# definindo a porcentagem de corte
pct_de_corte = 0.005 # valor = 0,5%

# menor e maior valores de corte
maiorCorte = round( (quadranteSantaLuzia + pct_de_corte) * len(baseProp) )
menorCorte = round( (quadranteSantaLuzia - pct_de_corte) * len(baseProp) )

# lista dos valores de corte
lista_prop_similares = [int(i) for i in range ( menorCorte, maiorCorte + 1 )]

# numero de municipios selecionados
n_selecionados = len(lista_prop_similares)

# lista de municipios agrupados por baseProp
baseProp_agrupada = baseProp.loc[lista_prop_similares,['codigo', 'municipio', 'valor_pct', 'Sigla']]
baseProp_agrupada = pd.read_excel("Informacoes_grupos/Demografia/cidades.xlsx")

# Criando base com os grupos de municipios ========================================================
baseProp_agrupada.insert (0, 'grupo', 'Grupo_1 - PropPretos')
idh_agrupada.insert (0, 'grupo', 'Grupo_2 - IDH')

municipios_proximos = [
    "Indiaroba",
    "Cristinápolis",
    "Estância",
    "Umbaúba",
    "Arauá",
    "Tomar do Geru",
    "Itabaianinha",
    'Santa Luzia do Itanhy',
    "Pedrinhas",
    "Boquim",
    "Salgado",
    "Lagarto",
    "Riachão do Dantas",
    "Simão Dias",
    "Poço Verde",
    "Tobias Barreto",
    "Itapicuru"
]

# realizando o merge ==============================================================================
municipios_proximos = pd.DataFrame( {'municipio': municipios_proximos, 'grupo': 'Grupo_3 - Proximidade'})


# Grupo 1 - Proximidade ---------------------------------------------

# realizando a captura dos dados para cada grupo
# Saude ----
proximosTotalInfo = municipios_proximos.merge(idh[['codigo','municipio','IDH','Sigla']], on='municipio', how='left')
proximosTotalInfo = proximosTotalInfo.merge(espVida[['codigo','esperanca_vida']], on='codigo', how='left')

# Demografia ----
proximosTotalInfo = proximosTotalInfo.merge(baseProp[['codigo','valor_pct']], on='codigo', how='left')
proximosTotalInfo = proximosTotalInfo.merge(demogr[['codigo','numeroPessoas']], on='codigo', how='left')

# Educacionais ----
proximosTotalInfo = proximosTotalInfo.merge(expEstudo[['codigo','anos_estudo']], on='codigo', how='left')
proximosTotalInfo = proximosTotalInfo.merge(txAnalf[['codigo','taxa_analfabetismo']], on='codigo', how='left')

# Emprego e Renda ----
proximosTotalInfo = proximosTotalInfo.merge(perCapta[['codigo','renda_percapta']], on='codigo', how='left')
proximosTotalInfo = proximosTotalInfo.merge(txDesemp[['codigo','tx_desemprego']], on='codigo', how='left')


# Grupo 2 - PropPretos ----------------------------------------------
# fazendo o mesmo para os demais muni
# realizando a captura dos dados para cada grupo
# Saude ----
basePropTotal = baseProp_agrupada.merge(idh[['codigo', 'IDH']], on='codigo', how='left')
basePropTotal = basePropTotal.merge(espVida[['codigo','esperanca_vida']], on='codigo', how='left')

# Demografia ----
basePropTotal = basePropTotal.merge(demogr[['codigo','numeroPessoas']], on='codigo', how='left')

# Educacionais ----
basePropTotal = basePropTotal.merge(expEstudo[['codigo','anos_estudo']], on='codigo', how='left')
basePropTotal = basePropTotal.merge(txAnalf[['codigo','taxa_analfabetismo']], on='codigo', how='left')

# Emprego e Renda ----
basePropTotal = basePropTotal.merge(perCapta[['codigo','renda_percapta']], on='codigo', how='left')
basePropTotal = basePropTotal.merge(txDesemp[['codigo','tx_desemprego']], on='codigo', how='left')


# Grupo 3 - IDH -----------------------------------------------------
# fazendo o mesmo para os demais muni
# realizando a captura dos dados para cada grupo
# Saude ----
idhTotal = idh_agrupada.merge(espVida[['codigo','esperanca_vida']], on='codigo', how='left')

# Demografia ----
idhTotal = idhTotal.merge(demogr[['codigo','numeroPessoas']], on='codigo', how='left')
idhTotal = idhTotal.merge(baseProp[['codigo','valor_pct']], on='codigo', how='left')

# Educacionais
idhTotal = idhTotal.merge(expEstudo[['codigo','anos_estudo']], on='codigo', how='left')
idhTotal = idhTotal.merge(txAnalf[['codigo','taxa_analfabetismo']], on='codigo', how='left')

# Emprego e Renda ----
idhTotal = idhTotal.merge(perCapta[['codigo','renda_percapta']], on='codigo', how='left')
idhTotal = idhTotal.merge(txDesemp[['codigo','tx_desemprego']], on='codigo', how='left')

# Grupo 4 - SANTA LUZIA ---------------------------------------------
santaLuziaTotal = idhTotal.loc[idhTotal.codigo == 2806305]
santaLuziaTotal['grupo'] = 'Grupo_4 - Santa Luzia do Itanhy'

# removendo as linhas de Santa Luzia dos grupos
idhTotal = idhTotal.drop(idhTotal.loc[idhTotal['codigo'] == 2806305].index)
basePropTotal = basePropTotal.drop(basePropTotal.loc[basePropTotal['codigo'] == 2806305].index)
proximosTotalInfo = proximosTotalInfo.drop(proximosTotalInfo.loc[proximosTotalInfo['codigo'] == 2806305].index)

# Grupo 5 - Isolados -------------------------------------------------
isolados = pd.read_csv('Informacoes_grupos/grupo_isolados.csv', sep = ';')
print(isolados)
isolados.insert (0, 'grupo', 'Grupo_5 - Isolados')

# Saude ----
isolados = isolados.merge(idh[['codigo','IDH','Sigla']], on='codigo', how='left')
isolados = isolados.merge(espVida[['codigo','esperanca_vida']], on='codigo', how='left')

# Demografia ----
isolados = isolados.merge(demogr[['codigo','numeroPessoas']], on='codigo', how='left')
isolados = isolados.merge(baseProp[['codigo','valor_pct']], on='codigo', how='left')

# Educacionais
isolados = isolados.merge(expEstudo[['codigo','anos_estudo']], on='codigo', how='left')
isolados = isolados.merge(txAnalf[['codigo','taxa_analfabetismo']], on='codigo', how='left')

# Emprego e Renda ----
isolados = isolados.merge(perCapta[['codigo','renda_percapta']], on='codigo', how='left')
isolados = isolados.merge(txDesemp[['codigo','tx_desemprego']], on='codigo', how='left')



# Salvando os dados em uma planilha com cada grupo em uma pasta =================================== 
writer = pd.ExcelWriter('bases_produzidas/informacoes_grupos_THP.xlsx', engine='xlsxwriter')

basePropTotal.to_excel(writer, sheet_name='Grupo_1 - PropPretos')
idhTotal.to_excel(writer, sheet_name='Grupo_2 - IDH')
proximosTotalInfo.to_excel(writer, sheet_name='Grupo_3 - Proximidade')
santaLuziaTotal.to_excel(writer, sheet_name='Grupo_4 - Santa Luzia do Itanhy')
isolados.to_excel(writer, sheet_name='Grupo_5 - Isolados')

writer.close() 

# juntando os data.frames
totalMunicipios = pd.concat([basePropTotal,idhTotal,proximosTotalInfo,santaLuziaTotal,isolados], ignore_index=True)

# adicionando municipios modificados para merge
totalMunicipios['municipio_merge'] = totalMunicipios['municipio'] + ' (' + totalMunicipios['Sigla'] + ')' 

# salvando as bases totais
totalMunicipios.to_csv('bases_produzidas/totalGruposMunicipios.csv', index=False, sep=';')

# bases de identificacao de grupo
totalMunicipios[['grupo','codigo','municipio','municipio_merge','Sigla']].to_csv('bases_produzidas/totalGruposMunicipiosIdentificadores.csv', index=False, sep=';')
