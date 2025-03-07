
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar com o Google Finance
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
            background-color: #0e0e0e;
        }
        .stock-title {
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 5px;
        }
        .price-container {
            font-size: 36px;
            font-weight: bold;
            color: white;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .price-change-positive {
            color: #34A853 !important;
            font-size: 24px !important;
            font-weight: bold;
        }
        .price-change-negative {
            color: #EA4335 !important;
            font-size: 24px !important;
            font-weight: bold;
        }
        .timestamp {
            font-size: 14px;
            color: #999999;
        }
    </style>
""", unsafe_allow_html=True)

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    try:
        # Buscar dados da ação
        stock = yf.Ticker(ticker)
        stock_info = stock.info  

        # Verificar se os dados são válidos
        if not stock_info or "longName" not in stock_info:
            raise ValueError("Ação não localizada")  # Dispara erro controlado

        company_name = stock_info.get("longName", ticker)
        moeda = stock_info.get("currency", "N/A")  # Obtém a moeda da ação

        # Exibir o nome completo da ação
        st.markdown(f'<p class="stock-title">{company_name} ({ticker})</p>', unsafe_allow_html=True)

        # Preço atual e variação
        preco_atual = stock_info.get("regularMarketPrice", None)
        preco_anterior = stock_info.get("previousClose", None)

        if preco_atual and preco_anterior:
            variacao = preco_atual - preco_anterior
            porcentagem = (variacao / preco_anterior) * 100
            cor_variacao = "price-change-positive" if variacao > 0 else "price-change-negative"
            simbolo_variacao = "▲" if variacao > 0 else "▼"

            # Horário do fechamento do mercado
            horario_fechamento = stock_info.get("regularMarketTime", None)
            if horario_fechamento:
                from datetime import datetime
                horario = datetime.utcfromtimestamp(horario_fechamento).strftime('%d %b, %I:%M %p GMT-3')
                horario_texto = f"At close: {horario}"
            else:
                horario_texto = ""

            st.markdown(f"""
                <div class="price-container">
                    {preco_atual:.2f} {moeda} 
                    <span class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%)</span>
                </div>
                <p class="timestamp">{horario_texto}</p>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Ação não localizada, insira o código de uma ação existente.")
