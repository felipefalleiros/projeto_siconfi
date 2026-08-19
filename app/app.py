# app.py

import streamlit as st

st.set_page_config(
    page_title="Ranking SICONFI",
    page_icon="📊",
    layout="wide"
)

# st.title("Ranking SICONFI")

# st.write("Selecione uma análise no menu lateral.")


pages = {
    "Gráficos":[
        st.Page("pages/evolucao_do_ranking.py", title='Evolução do Ranking'),
        st.Page("pages/analise_das_verificacoes.py", title='Análise das Verificações')
        ]
    }

pg = st.navigation(pages)
pg.run()