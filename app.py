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
            text-align: left;  /* Alinhado à esquerda */
            margin: 10px 10px 20px 0px;
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
            .period-selector {
                text-align: center;
            }
            .period-selector span {
                display: inline-block;
                padding: 4px 5px;
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

    # Buscar setor da empresa (agora em inglês, sem tradução)
    setor_en = stock.info.get("sector", "Sector not found")

    # Exibir nome da ação e setor corretamente
    st.subheader(ticker)
    st.markdown(f'<div class="sector-text">Sector: {setor_en}</div>', unsafe_allow_html=True)

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

    # Criando os botões interativos usando Streamlit
    colunas = st.columns(len(periodos))  # Criar colunas para cada período
    for i, (p, v) in enumerate(periodos.items()):
        with colunas[i]:  # Criando botões interativos
            if st.button(p, key=f"period_{p}"):
                st.session_state["periodo_selecionado"] = p

    # Atualizar os dados com base no período selecionado
    periodo = periodos[st.session_state["periodo_selecionado"]]
    dados = stock.history(period=periodo)

    # Criar gráfico no estilo Google Finance
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#4285F4', width=2),
        fill='tozeroy',  # Efeito de preenchimento como no Google Finance
        fillcolor='rgba(66, 133, 244, 0.2)'  
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
