#!/usr/bin/env python
# coding: utf-8

# In[85]:


import pandas as pd

# Carrega a base de dados do arquivo CSV

dados = pd.read_csv('Relação de Contratos.csv', sep=';', engine= 'python', encoding='latin-1', on_bad_lines='skip')

dados = dados[dados["Modalidade"] == "Eventual"]

# Filtra a coluna "G" com somente valores especificados
valores_G = ["D", "FX", "FY", "G", "H" ,"HX", "HW" ,"HY", "HZ", "I", "J", "K", "KX", "M", "MJ", "MR", "MS", "ME", "SS", "SY", "SX", "XE", "JC", "KE", "QX","T", "E", "L", "LX"]
dados = dados[dados["Grupo"].isin(valores_G)]

# Filtra a coluna "AO" com somente valores especificados
valores_AO = ["Upgrade", "UpSell"]
dados = dados[dados["Upgrade"].isin(valores_AO)]

valores_AA = ["Aberto"]
dados = dados[dados["Status do Período"].isin(valores_AA)]

lojas = pd.read_csv('lojas.csv', sep=';', engine= 'python', encoding='latin-1', on_bad_lines='skip', usecols=['Filial ID', 'Loja', 'Região'], index_col='Filial ID')

# Adiciona a coluna com o nome da loja

dados['Loja Retirada'] = dados['Loja RET'].apply(lambda x: lojas.loc[x]['Loja'])

dados['Loja Devolução'] = dados['Loja DEV'].apply(lambda x: lojas.loc[x]['Loja'])

dados['Região Retirada'] = dados['Loja RET'].apply(lambda x: lojas.loc[x]['Região'])

dados['Região Devolução'] = dados['Loja DEV'].apply(lambda x: lojas.loc[x]['Região'])

dados = dados.drop(['Grupo Econômico', 'Sequência', 'Última alteração de Grupo',"Início do Período", "Início do Período",
                    "Fim do Período", "Status Geral","Tarifa", "Responsabilidade", "CPF do Agente", "Agente", 
                    "AgenteID", "Email do Agente", "Programa de Incentivo Movida", "Total da Sequência", "Total do Acordo", 
                    "Total TXAdm", "Valor Pago", "Status do Pag.","Cliente", "Empresa", "Agência", "CNPJ Agência", 
                    "Abertura", "Fechamento Período", "Fechamento Contrato","KM Rodado", 
                    "Data Fechamento Contrato", "   Franquia diária", "Unnamed: 43"], axis=1)

coluna_copia = dados['Grupo'].copy()

dados.insert(loc=7, column='Grupo Retirada', value=coluna_copia)

dados = dados.drop(["Grupo"], axis=1)

dados['Loja RET'] = dados['Loja Retirada']
dados['Loja DEV'] = dados['Loja Devolução']

dados = dados.drop(['Loja Retirada', 'Loja Devolução'], axis=1)

dados = dados.rename(columns={'Status do Período': 'Status'})
dados = dados.rename(columns={'Upgrade': 'Upgrade/Upsell'})

dados.to_csv('Relatório.csv', index=False, sep=';', encoding='latin-1')


#display(dados)
#display(lojas)

