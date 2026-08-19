import pandas as pd

def carregar_dados_ranking():
   return pd.read_csv('dados/dados_fonte/municipios_bspn_base.csv', sep=';')

def carregar_descricao_verificacoes():
   return pd.read_csv('dados/dados_fonte/Descricao_verificacoes.csv', sep=';')

def carregar_aplicabilidade_verificacoes():
   return pd.read_csv('dados/dados_fonte/Aplicabilidade_verificacoes.csv', sep=';')