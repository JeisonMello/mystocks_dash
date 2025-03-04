import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Caixa de seleção para escolher uma ação
ticker = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")
# Entrada do usuário
ticker = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

# ✅ Adiciona automaticamente o sufixo ".SA" para ações brasileiras
if ticker:  # Verifica se o usuário digitou algo antes de modificar o ticker
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")  # 10 anos de histórico


    # Exibir tabela de dados básicos
    st.subheader(f"📊 Dados Gerais da Ação: {ticker}")
    st.write(dados.tail(10))  # Exibir as últimas 10 linhas

    # Criar gráfico da cotação ao longo dos anos
    st.subheader("📈 Histórico de Preços")
    fig = px.line(dados, x=dados.index, y="Close", title=f"Evolução do Preço - {ticker}")
    st.plotly_chart(fig)

    # Buscar e exibir dividendos
    st.subheader("💰 Dividendos Anuais")
    dividendos = stock.dividends.resample("Y").sum()
    fig_divid = px.bar(x=dividendos.index, y=dividendos.values, title="Valor Pago em Dividendos Anualmente")
    st.plotly_chart(fig_divid)
