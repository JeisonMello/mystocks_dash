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
        .price-change-positive {
            color: #34A853 !important;
            font-size: 20px !important;
        }
        .price-change-negative {
            color: #EA4335 !important;
            font-size: 20px !important;
        }
        .period-container {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 8px 0;
            gap: 15px;
        }
        .period-selector {
            font-size: 16px;
            font-weight: 600;
            color: #ccc;
            cursor: pointer;
            padding: 4px 8px;
            transition: color 0.2s ease-in-out, background 0.2s ease-in-out;
            user-select: none;
            background-color: transparent;
            border-bottom: 3px solid transparent;
        }
        .period-selector:hover {
            color: #ffffff;
        }
        .selected-period {
            color: #ffffff;
            border-bottom: 3px solid #4285F4;
            padding-bottom: 2px;
            background-color: transparent;
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
            <div class='title-container'>{ticker} ·</div>
            <h2 class='stock-title'>{company_name}</h2>
        """, unsafe_allow_html=True)

        # ==========================
        # SELETOR DE PERÍODO HORIZONTAL (FUNCIONAL)
        # ==========================
        periodos = {
            "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
            "YTD": "ytd", "1Y": "1y", "5Y": "5y", "ALL": "max"
        }

        if "periodo_selecionado" not in st.session_state:
            st.session_state["periodo_selecionado"] = "6M"

        colunas = st.columns(len(periodos))
        for i, (p, v) in enumerate(periodos.items()):
            with colunas[i]:
                if st.button(p, key=p):
                    st.session_state["periodo_selecionado"] = p

        periodo = periodos[st.session_state["periodo_selecionado"]]
        dados = stock.history(period=periodo)

        # ==========================
        # CÁLCULO DE VARIAÇÃO DO PREÇO COM PRECISÃO YAHOO
        # ==========================
        preco_atual = stock_info.get("regularMarketPrice", None)
        preco_anterior = stock_info.get("previousClose", None)
        if preco_atual and preco_anterior:
            variacao = preco_atual - preco_anterior
            porcentagem = (variacao / preco_anterior) * 100
            cor_variacao = "price-change-positive" if variacao > 0 else "price-change-negative"
            simbolo_variacao = "▲" if variacao > 0 else "▼"
            st.markdown(f"""
                <p class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%)</p>
            """, unsafe_allow_html=True)

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
