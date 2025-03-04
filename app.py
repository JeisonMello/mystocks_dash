import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar elementos ao estilo do Google Finance
st.markdown("""
    <style>
        div[data-testid="stButton"] > button {
            background-color: transparent !important;
            border: none !important;
            color: #cccccc !important;
            font-size: 16px !important;
            font-weight: normal !important;
            padding: 6px 15px !important;
            text-transform: none !important;
        }
        div[data-testid="stButton"] > button:hover {
            color: #ffffff !important;
            border-bottom: 2px solid #4285F4 !important;
        }
        div[data-testid="stButton"] > button:focus {
            color: #4285F4 !important;
            border-bottom: 2px solid #4285F4 !important;
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
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)

    # 📌 Adicionar uma linha separadora antes dos botões de período
    st.markdown("<hr>", unsafe_allow_html=True)

    # Botões de período para histórico de preços
    periodos = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD":
