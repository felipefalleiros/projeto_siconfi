import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def carregar_dados():
    return pd.read_parquet(
        "dados/dados_tratados/dados_siconfi.parquet"
    )


df = carregar_dados()


def calcular_media_estadual(df, exercicio, estado):
    df_filtrado = df[
        (df['exercicio'] == exercicio) &
        (df['estado'] == estado) &
        (df['aplicavel'] == True)
    ]

    return (
        df_filtrado
        .groupby('verificacao', as_index=False)['nota']
        .mean()
        .rename(columns={'nota': 'media_estadual'})
    )
    
def destacar_nota(row):
    cor = (
        "green"
        if row["nota"] >= row["media_estadual"]
        else "red"
    )

    return pd.Series({
        "nota": f"color: {cor}"
    })

st.title("Análise das Verificações")

# -------------------------
# Filtro de Exercício
# -------------------------

exercicios = sorted(
    df["exercicio"].unique()
)

exercicio_selecionado = st.selectbox(
    "Exercício",
    exercicios
)


# -------------------------
# Filtro de estado
# -------------------------

estados = sorted(
    df["estado"]
    .unique()
)

estado_selecionado = st.selectbox(
    "Estado",
    estados
)


# -------------------------
# Filtro de município
# -------------------------

df_estado = df[
    df["estado"] == estado_selecionado
]

municipios = sorted(
    df_estado["municipio"]
    .unique()
)

municipio_selecionado = st.selectbox(
    "Município",
    municipios
)

# -------------------------
# Filtro de dimensão
# -------------------------

dimensoes = sorted(
    df["dimensao"].unique()
)

dimensao_selecionada = st.selectbox(
    "Dimensão",
    dimensoes
)

# -------------------------
# Dados do município
# -------------------------

df_municipio = df_estado[
    (df_estado["municipio"] == municipio_selecionado)  &
    (df_estado["exercicio"] == exercicio_selecionado) &
    (df_estado["dimensao"] == dimensao_selecionada) &
    (df_estado["aplicavel"] == True)
].copy()

df_media = calcular_media_estadual(df, exercicio_selecionado, estado_selecionado)

df_exibicao = df_municipio.merge(
    df_media,
    on="verificacao",
    how="left"
)

df_tabela = (
    df_exibicao[
        ["verificacao", "descricao", "nota", "media_estadual"]
    ]
    .style
    .apply(destacar_nota, axis=1)
)

container = st.container(border=True)

with container:
    
    
    st.dataframe(
        df_tabela,
        hide_index=True,
        column_config={
            "verificacao":"Verificação",
            "descricao":"Descrição",
            "nota": st.column_config.NumberColumn("Nota", format="%.2f"),
            "media_estadual": st.column_config.NumberColumn("Média estadual", format="%.2f")
        },
        use_container_width=True
    )
    
        
# df_dimensoes = df[
#     (df["exercicio"] == exercicio_selecionado) &
#     (df["aplicavel"] == True)
# ]

# dimensoes = sorted(df_dimensoes ["dimensao"].unique())

# dimensao_selecionada = st.selectbox(
#     "Dimensão",
#     dimensoes
# )