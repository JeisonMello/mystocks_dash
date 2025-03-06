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
            font-weight: normal !important;
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
        .title-container {
            font-size: 18px;
            color: #666;
            text-transform: uppercase;
        }
        .stock-title {
            font-size: 26px;
            font-weight: 500;
            color: #222;
        }
    </style>
""", unsafe_allow_html=True)

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    stock_info = stock.info  
    dados = stock.history(period="10y")

    if not stock_info or "longName" not in stock_info:
        st.error("Ação não encontrada! Verifique o código e tente novamente.")
    else:
        company_name = stock_info.get("longName", ticker)
        market = stock_info.get("exchange", "BVMF")  # Define BVMF como padrão
        st.markdown(f"""
            <div class='title-container'>HOME > {ticker} · {market}</div>
            <h2 class='stock-title'>{company_name}</h2>
        """, unsafe_allow_html=True)

        # ==========================
        # HISTÓRICO DE PREÇOS
        # ==========================
        st.subheader(f"Histórico de Preços - {ticker}")
        fig_price = go.Figure()

        fig_price.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color='#4285F4', width=2),
            fillcolor='rgba(66, 133, 244, 0.2)'
        ))

        fig_price.update_layout(
            template="plotly_white",
            title=f"Evolução do Preço - {ticker}",
            xaxis_title="Ano",
            yaxis_title="Preço (R$)",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="black"),
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)")
        )

        st.plotly_chart(fig_price)
