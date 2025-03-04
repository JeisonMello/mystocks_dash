import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

# Botões de período para histórico de preços (agora no estilo do Google Finance)
periodos = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"}

# Criando os botões de período como texto clicável
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
botoes = [col1, col2, col3, col4, col5, col6, col7, col8]
periodo_selecionado = "6M"  # Padrão inicial

for i, (label, value) in enumerate(periodos.items()):
    if botoes[i].button(label, key=f"btn_{label}"):
        periodo_selecionado = label  # Atualiza o período quando um botão é clicado

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period=periodos[periodo_selecionado])

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
        {preco_atual:.2f} BRL {simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) nos últimos {periodo_selecionado}
    </h2>
    """, unsafe_allow_html=True)

    # 📌 Gráfico de Preços - Linha Azul Royal, com Suavização
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#3454b4', width=2),  # Azul royal claro, mais fino e elegante
        fill='tozeroy',
        fillcolor='rgba(52, 84, 180, 0.2)'  # Transparência suave no fundo
    ))

    # Ajuste na escala para não encostar no zero
    min_preco = dados["Close"].min()
    max_preco = dados["Close"].max()
    margem = (max_preco - min_preco) * 0.1  # Adiciona uma margem de 10%

    fig_price.update_layout(
        template="plotly_dark",
        title=f"Evolução do Preço - {periodo_selecionado} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)", range=[min_preco - margem, max_preco + margem])  # Ajuste da proporção correta
    )

    st.plotly_chart(fig_price)
