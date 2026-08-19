import pandas as pd

def exportar_dados_siconfi(df):

    df.to_parquet(
        'dados/dados_tratados/dados_siconfi.parquet',
        index=False
    )


def exportar_ranking(df):

    df.to_parquet(
        'dados/dados_tratados/dados_ranking_siconfi.parquet',
        index=False
    )