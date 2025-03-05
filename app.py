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
        }
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
        .period-selector {
            font-size: 16px;
            font-weight: 600;
            color: #ccc;
            text-align: center;
            margin: 10px 0;
        }
        .selected-period {
            color: #4285F4;
            border-bottom: 3px solid #4285F4;
            padding-bottom: 2px;
        }
        .sector-text {
            font-size: 18px;
            font-weight: 500;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("Dashboard da Ação")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")

    # Buscar setor da empresa
    setor_en = stock.info.get("sector", "Setor não encontrado")

    # Tradução do setor para português
    setores_traduzidos = {
        "Consumer Cyclical": "Consumo Cíclico",
        "Financial Services": "Serviços Financeiros",
        "Technology": "Tecnologia",
        "Industrials": "Indústria",
        "Healthcare": "Saúde",
        "Basic Materials": "Materiais Básicos",
        "Consumer Defensive": "Consumo Defensivo",
        "Utilities": "Serviços Públicos",
        "Energy": "Energia",
        "Real Estate": "Imóveis",
        "Communication Services": "Serviços de Comunicação"
    }
    setor_pt = setores_traduzidos.get(setor_en, setor_en)  # Mantém em inglês se não encontrar tradução

    # Exibir nome da ação e setor corretamente
    st.subheader(ticker)
    st.markdown(f'<div class="sector-text">Setor: {setor_pt}</div>', unsafe_allow_html=True)

    # =====================================
    # HISTÓRICO DE PREÇOS
    # =====================================
    st.subheader(f"Histórico de Preços")

    # Botões de período
    periodos = {
        "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
        "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"
    }

    # Criando a linha de seleção de período
    periodo_keys = list(periodos.keys())
    periodo_selecionado = st.session_state.get("periodo_selecionado", "6M")

    # Criando linha de período customizada em HTML
    periodo_html = '<div class="period-selector">'
    for p in periodo_keys:
        if p == periodo_selecionado:
            periodo_html += f'<span class="selected-period">{p}</span> | '
        else:
            periodo_html += f'<span>{p}</span> | '
    periodo_html = periodo_html.rstrip(" | ")  # Remove o último "|"
    periodo_html += '</div>'

    st.markdown(periodo_html, unsafe_allow_html=True)

    # Atualizar os dados com base no período
    periodo = periodos[periodo_selecionado]
    dados = stock.history(period=periodo)

    # Criar gráfico no estilo Google Finance
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#4285F4', width=2)
    ))

    fig_price.update_layout(
        template="plotly_white",
        xaxis_title="",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_price)
