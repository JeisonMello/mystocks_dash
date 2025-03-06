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
            background-color: #0e0e0e;
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
        st.markdown(f"""
            <div class='title-container'>Histórico de Preços</div>
            <h2 class='stock-title'>{company_name}</h2>
        """, unsafe_allow_html=True)

        # ==========================
        # PREÇO ATUAL, VARIAÇÃO E HORÁRIO DE FECHAMENTO
        # ==========================
        preco_atual = stock_info.get("regularMarketPrice", None)
        preco_anterior = stock_info.get("previousClose", None)
        horario_fechamento = stock_info.get("regularMarketTime", None)
        if preco_atual and preco_anterior:
            variacao = preco_atual - preco_anterior
            porcentagem = (variacao / preco_anterior) * 100
            cor_variacao = "price-change-positive" if variacao > 0 else "price-change-negative"
            simbolo_variacao = "▲" if variacao > 0 else "▼"
            
            st.markdown(f"""
                <div class="price-container">
                    {preco_atual:.2f} BRL 
                    <span class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%)</span>
                </div>
            """, unsafe_allow_html=True)

            if horario_fechamento:
                from datetime import datetime
                horario = datetime.utcfromtimestamp(horario_fechamento).strftime('%d %b, %I:%M %p GMT-3')
                st.markdown(f"<p class='timestamp'>At close: {horario}</p>", unsafe_allow_html=True)

        # ==========================
        # HISTÓRICO DE PREÇOS COM ZOOM AUTOMÁTICO PARA ESCALA CORRETA
        # ==========================
        cor_grafico = "#34A853" if variacao > 0 else "#EA4335"
        transparencia = "rgba(52, 168, 83, 0.2)" if variacao > 0 else "rgba(234, 67, 53, 0.2)"

        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color=cor_grafico, width=2),
            fillcolor=transparencia
        ))

        # Aplicar zoom automático para manter a escala proporcional ao Yahoo Finance
        fig_price.update_layout(
            modebar_remove=['zoom', 'pan', 'reset', 'select', 'lasso', 'zoomIn', 'zoomOut', 'autoScale', 'home'], 
            template="plotly_white",
            xaxis_title="Ano",
            yaxis_title="Preço (R$)",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="black"),
            xaxis=dict(showgrid=False, range=[dados.index.min(), dados.index.max()]),
            yaxis=dict(range=[dados["Close"].min() * 0.95, dados["Close"].max() * 1.05],
                       showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)")
        )

        st.plotly_chart(fig_price)
