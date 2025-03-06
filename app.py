import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar os elementos ao estilo do Google Finance
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        body {
            font-family: 'Inter', sans-serif;
        }
        h2 {
            font-size: 32px !important;
            font-weight: bold !important;
            margin-bottom: 0px !important;
        }
        .subtext {
            font-size: 20px !important;
            font-weight: normal !important;
            color: #999999 !important;
        }
        .positive {
            color: #34A853 !important;
            font-size: 20px !important;
        }
        .negative {
            color: #EA4335 !important;
            font-size: 20px !important;
        }
        hr {
            border: 0;
            height: 1px;
            background: #666;
            margin: 10px 0 10px 0;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("📊 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")

    if not dados.empty:
        # Buscar preço atual
        preco_atual = dados["Close"].iloc[-1]
        preco_anterior = dados["Close"].iloc[0]
        variacao = preco_atual - preco_anterior
        porcentagem = (variacao / preco_anterior) * 100
        cor_variacao = "positive" if variacao > 0 else "negative"
        simbolo_variacao = "▲" if variacao > 0 else "▼"

        # Exibir o preço da ação seguindo o padrão do Google Finance
        st.markdown(f"""
            <h2>{preco_atual:.2f} BRL <span class="subtext">BRL</span></h2>
            <p class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) hoje</p>
        """, unsafe_allow_html=True)

        # =====================================
        # 📌 HISTÓRICO DE PREÇOS
        # =====================================
        st.subheader(f"📈 Histórico de Preços - {ticker}")
        fig_price = go.Figure()

        fig_price.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',  # Preenchimento suave
            line=dict(color='#4285F4', width=2),  # Azul Google Finance mais fino
            fillcolor='rgba(66, 133, 244, 0.2)'  # Transparência suave no fundo
        ))

        fig_price.update_layout(
            template="plotly_white",
            title=f"Evolução do Preço - {ticker}",
            xaxis_title="Ano",
            yaxis_title="Preço (R$)",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
            paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico
            font=dict(color="black"),  # Texto preto para melhor contraste
            xaxis=dict(showgrid=False),  # Remove grade vertical
            yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)")  # Grade cinza suave
        )

        st.plotly_chart(fig_price)
    else:
        st.warning(f"⚠️ Nenhuma informação de preços encontrada para {ticker}.")
