import streamlit as st
from precos.app_precos import carregar_grafico_precos

st.title("Histórico de Preços 📈")

# Entrada do usuário para o ticker da ação
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker:
    fig_precos = carregar_grafico_precos(ticker)

    if fig_precos:
        st.plotly_chart(fig_precos)
    else:
        st.error("Erro ao carregar o gráfico de preços.")
