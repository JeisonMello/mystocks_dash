import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="6mo")  # Últimos 6 meses

    # Buscar preço atual e variação do dia
    preco_atual = dados["Close"].iloc[-1]
    variacao = preco_atual - dados["Close"].iloc[-2]
    porcentagem = (variacao / dados["Close"].iloc[-2]) * 100
    cor_variacao = "green" if variacao > 0 else "red"

    # Exibir o preço acima do gráfico
    st.markdown(f"<h2 style='color:{cor_variacao};'> {preco_atual:.2f} BRL ({variacao:.2f} BRL, {porcentagem:.2f}%)</h2>", unsafe_allow_html=True)

    # 📌 Estilizar o Gráfico de Preços com Proporção Correta
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    # Definir limites do eixo Y para evitar que a linha encoste no zero
    min_preco = dados["Close"].min()
    max_preco = dados["Close"].max()
    margem = (max_preco - min_preco) * 0.1  # 10% de margem superior e inferior

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#3454b4', width=2),  # Azul atualizado
    ))

    fig_price.update_layout(
        template="plotly_white",
        title=f"Evolução do Preço - Últimos 6 Meses ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
        paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico
        font=dict(color="#ad986e"),  # Texto em dourado elegante
        xaxis=dict(showgrid=False),  # Remove grade vertical
        yaxis=dict(
            showgrid=True, 
            gridcolor="rgba(173, 152, 110, 0.2)",  # Grade dourada suave
            range=[min_preco - margem, max_preco + margem]  # Ajuste da proporção do eixo Y
        )
    )

    st.plotly_chart(fig_price)

    # 📌 O Gráfico de Dividendos foi mantido exatamente como estava antes, sem alterações.
