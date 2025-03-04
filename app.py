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

    # Buscar preço atual e variação percentual
    preco_atual = dados["Close"].iloc[-1]
    preco_anterior = dados["Close"].iloc[0]
    variacao = preco_atual - preco_anterior
    porcentagem = (variacao / preco_anterior) * 100
    cor_variacao = "green" if variacao > 0 else "red"
    simbolo_variacao = "🔼" if variacao > 0 else "🔻"

    # Exibir valor atual e variação percentual no topo
    st.markdown(f"""
    <h2 style='color:{cor_variacao};'>
        {preco_atual:.2f} BRL {simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) nos últimos 6 meses
    </h2>
    """, unsafe_allow_html=True)

    # 📌 Gráfico de Preços - Linha mais fina e elegante
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#d62828', width=1.8),  # Vermelho refinado, linha mais fina e suave
        fill='tozeroy',
        fillcolor='rgba(214, 40, 40, 0.2)'  # Fundo com transparência sutil
    ))

    fig_price.update_layout(
        template="plotly_dark",
        title=f"Evolução do Preço - Últimos 6 Meses ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)")  # Grade discreta
    )

    st.plotly_chart(fig_price)
