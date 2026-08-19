import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def carregar_dados():
    return pd.read_parquet(
        "dados/dados_tratados/dados_ranking_siconfi.parquet"
    )


df = carregar_dados()


st.title("Ranking SICONFI")

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
    df_estado["municipio"] == municipio_selecionado
].copy()

df_municipio = df_municipio.sort_values(
    "exercicio"
)


# -------------------------
# Gráfico
# -------------------------

fig = px.line(
    df_municipio,
    x="exercicio",
    y="class_ranking",
    markers=True,
    labels={
        "exercicio": "Ano",
        "class_ranking": "Posição no ranking"
    },
    title=f"Evolução do ranking — {municipio_selecionado}"
)

fig.update_yaxes(
    autorange="reversed"
)

fig.update_traces(
    textposition="top center",
    hovertemplate=(
        "<b>Ano:</b> %{x}<br>"
        "<b>Posição:</b> %{y}<br>"
        "<b>Nota:</b> %{customdata[0]}<extra></extra>"
    ),
    customdata=df_municipio[["nota_ranking"]].values
)

st.plotly_chart(
    fig,
    use_container_width=True
)