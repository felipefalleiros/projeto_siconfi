from src import ingestao
from src import tratamento
from src import exportacao


def main():

    dados_ranking = ingestao.carregar_dados_ranking()

    df_descricao = (
        ingestao.carregar_descricao_verificacoes()
    )

    df_aplicabilidade = (
        ingestao.carregar_aplicabilidade_verificacoes()
    )

    df_descricao = (
        tratamento.tratamento_descricao_verificacoes(
            df_descricao
        )
    )

    df_aplicabilidade = (
        tratamento.tratamento_aplicabilidade_verificacoes(
            df_aplicabilidade
        )
    )

    df_siconfi = (
        tratamento.tratamento_dados_siconfi(
            dados_ranking,
            df_aplicabilidade,
            df_descricao
        )
    )

    df_ranking = (
        tratamento.gerar_dados_ranking(
            df_siconfi
        )
    )

    exportacao.exportar_dados_siconfi(
        df_siconfi
    )

    exportacao.exportar_ranking(
        df_ranking
    )


if __name__ == '__main__':
    main()