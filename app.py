import streamlit as st
from precos.app_precos import carregar_grafico_precos
from dividendos.app_dividendos import carregar_grafico_dividendos

st.title("Dashboard de Ações 📈💰")

# Entrada do usuário para o ticker da ação
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker:
    # Exibir Gráfico de Preços
    st.subheader("📊 Histórico de Preços")
    fig_precos = carregar_grafico_precos(ticker)
    st.plotly_chart(fig_precos)

    # Exibir Gráfico de Dividendos
   
