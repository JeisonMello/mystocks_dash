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
        .period-selector {
            font-size: 16px;
            font-weight: 600;
            color: #ccc;
            text-align: center;
            margin: 10px 10px 20px 10px;
        }
        .period-selector span {
            padding: 6px 12px;
            cursor: pointer;
            transition: color 0.2s ease-in-out, border-bottom 0.2s ease-in-out;
            display: inline-block;
        }
        .period-selector span:hover {
            color: #ffffff;
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
        /* Responsividade */
        @media screen and (max-width: 600px) {
            .period-selector span {
                display: block;
                padding: 4px 0;
            }
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

    # Botões de período (agora interativos)
    periodos = {
        "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
        "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"
    }

    # Estado da seleção do período
    if "periodo_selecionado" not in st.session_state:
        st.session_state["periodo_selecionado"] = "6M"

    # Criando linha de período customizada em HTML
    periodo_html = '<div class="period-selector">'
    for p in periodos.keys():
        if p == st.session_state["periodo_selecionado"]:
            periodo_html += f'<span class="selected-period">{p}</span> | '
        else:
            periodo_html += f'<span onclick="selectPeriodo(\'{p}\')">{p}</span> | '
    periodo_html = periodo_html.rstrip(" | ")  # Remove o último "|"
    periodo_html += '</div>'

    # Exibir os períodos corretamente
    st.markdown(periodo_html, unsafe_allow_html=True)

    # Atualizar os dados com base no período selecionado
    periodo = periodos[st.session_state["periodo_selecionado"]]
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
        template="plotly_dark",
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
