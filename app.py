import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

# ✅ Verifica se o usuário digitou algo antes de modificar o ticker
if ticker_input:
    ticker = ticker_input  # Garante que estamos usando uma variável nova
    
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")  # 10 anos de histórico

    # ✅ Buscar setor da empresa
    setor = stock.info.get("sector", "Setor não encontrado")

    # Exibir setor da empresa
    st.subheader("🏢 Setor da Empresa")
    st.write(f"📌 **{setor}**")

    # Criar gráfico da cotação ao longo dos anos
    st.subheader("📈 Histórico de Preços")
    fig = px.line(dados, x=dados.index, y="Close", title=f"Evolução do Preço - {ticker}")
    st.plotly_chart(fig)

    # Buscar e exibir dividendos
    st.subheader("💰 Dividendos Anuais")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)  # Garante o formato datetime
        dividendos = stock.dividends.resample("Y").sum()

        fig_divid = px.bar(x=dividendos.index.year, y=dividendos.values, title="Valor Pago em Dividendos Anualmente")
        st.plotly_chart(fig_divid)
    else:
        st.warning("⚠️ Nenhuma informação de dividendos encontrada para esta ação.")
