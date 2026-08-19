import pandas as pd
import re
from . import ingestao

dados_ranking = ingestao.carregar_dados_ranking()
df_descricoes_verificacoes = ingestao.carregar_descricao_verificacoes()
df_aplicabilidade_verificacoes = ingestao.carregar_aplicabilidade_verificacoes()


def tratamento_descricao_verificacoes(df_descricoes_verificacoes):
    df_descricoes_verificacoes.rename(columns={'no_verificacao':'verificacao', 'no_desc':'descricao'}, inplace=True)
    
    return df_descricoes_verificacoes
    

def tratamento_aplicabilidade_verificacoes(df_aplicabilidade_verificacoes):
    df_aplicabilidade = df_aplicabilidade_verificacoes.rename(columns={'VERIFICACAO':'verificacao'})
    df_aplicabilidade.fillna('', inplace=True)
    
    return df_aplicabilidade

df_descricao = ingestao.carregar_descricao_verificacoes()
df_descricao = tratamento_descricao_verificacoes(df_descricao)

df_aplicabilidade = ingestao.carregar_aplicabilidade_verificacoes()
df_aplicabilidade = tratamento_aplicabilidade_verificacoes(df_aplicabilidade)


def tratamento_dados_siconfi(dados_ranking, df_aplicabilidade, df_descricao):
    

    verificacoes = [
        coluna for coluna in dados_ranking.columns
        if re.match(r'^D[1-4]_\d+$', coluna)
    ]

    data_verificacoes = dados_ranking.melt(
        id_vars=['exercicio', 'nome', 'sigla', 'class_ranking', 'nota_ranking'],
        value_vars=verificacoes,
        var_name='verificacao',
        value_name='nota'
    )

    data_verificacoes = data_verificacoes.sort_values(
        by=['exercicio','nome', 'verificacao']
    )

    df_siconfi = data_verificacoes.merge(
        df_aplicabilidade,
        on='verificacao',
        how='left'
    )

    df_siconfi = df_siconfi.merge(
        df_descricao,
        on='verificacao',
        how='left'
    )

    df_siconfi['dimensao'] = (
        df_siconfi['verificacao']
        .str[:2]
        .map({
            'D1': 'Dimensão 1',
            'D2': 'Dimensão 2',
            'D3': 'Dimensão 3',
            'D4': 'Dimensão 4'
        })
    )
    
    df_siconfi['aplicavel'] = df_siconfi.apply(
    lambda row: row[str(row['exercicio'])] != '',
    axis=1
    )
    
    df_siconfi.rename(columns={'nome':'municipio'}, inplace=True)
    df_siconfi.rename(columns={'sigla':'estado'}, inplace=True)
          
    return df_siconfi

def gerar_dados_ranking(df_siconfi):

    df_ranking = df_siconfi[
        ['exercicio','municipio','estado','class_ranking','nota_ranking']
    ].copy()

    df_ranking = (
        df_ranking
        .drop_duplicates()
        .sort_values(
            by=[
                'estado',
                'municipio',
                'exercicio'
            ]
        )
    )

    return df_ranking