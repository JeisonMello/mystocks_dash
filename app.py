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
    st.subheader("💰 Histórico de Dividendos")
    fig_dividendos, dados_dividendos = carregar_grafico_dividendos(ticker)

    if fig_dividendos:
        st.plotly_chart(fig_dividendos)
        st.write("**Tabela de Dividendos por Ano**")
        st.dataframe(dados_dividendos.rename(columns={"Ano": "Ano", "Dividends": "Dividendos Pagos"}))
    else:
        st.warning("Nenhum histórico de dividendos encontrado para esta ação.")
