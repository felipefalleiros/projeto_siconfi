import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def carregar_dados():
    return pd.read_parquet(
        "dados/dados_tratados/dados_siconfi.parquet"
    )


df = carregar_dados()


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
# Dados do município
# -------------------------

df_municipio = df_estado[
    (df_estado["municipio"] == municipio_selecionado)  &
    (df_estado["exercicio"] == exercicio_selecionado)
].copy()
