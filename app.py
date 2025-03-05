import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para remover aparência de botão e alinhar com Google Finance
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
        }
        .period-container {
            display: flex;
            align-items: center;
            justify-content: flex-start;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        }
        .period-selector {
            font-size: 16px;
            font-weight: 600;
            color: #ccc;
            cursor: pointer;
            padding: 8px 12px;
            transition: color 0.2s ease-in-out, border-bottom 0.2s ease-in-out;
            user-select: none;
        }
        .period-selector:hover {
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
        /* Remover borda dos botões abaixo */
        .invisible-button button {
            background: none !important;
            border: none !important;
            color: #ccc !important;
            font-size: 16px !important;
            font-weight: 600 !important;
            padding: 6px 12px !important;
            cursor: pointer;
        }
        .invisible-button button:hover {
            color: #ffffff !important;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("Dashboard da Ação")

# Entrada do usuário para selecionar uma ação
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)

    # Buscar setor da empresa (correção para ITSA4)
    setor_en = stock.info.get("sector", "Sector not found")
    
    # Corrigindo manualmente para ITSA4
    if ticker == "ITSA4.SA":
        setor_en = "Financial Services"

    # Exibir nome da ação e setor corretamente
    st.subheader(ticker)
    st.markdown(f'<div class="sector-text">Setor: {setor_en}</div>', unsafe_allow_html=True)

    # ==========================
    # HISTÓRICO DE PREÇOS
    # ==========================
    st.subheader(f"Histórico de Preços")

    # Definição dos períodos disponíveis
    periodos = {
        "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
        "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"
    }

    # Estado da seleção do período
    if "periodo_selecionado" not in st.session_state:
        st.session_state["periodo_selecionado"] = "6M"

    # Criando a barra de seleção com área clicável real
    periodo_html = '<div class="period-container">'
    for p, v in periodos.items():
        selected_class = "selected-period" if p == st.session_state["periodo_selecionado"] else ""
        periodo_html += f'<span class="period-selector {selected_class}" onclick="set_periodo(\'{p}\')">{p}</span> | '
    periodo_html = periodo_html.rstrip(" | ")  # Remove o último "|"
    periodo_html += '</div>'

    # Exibir os períodos corretamente
    st.markdown(periodo_html, unsafe_allow_html=True)

    # Criando uma segunda barra interativa sem aparência de botão
    cols = st.columns(8)
    for idx, (p, v) in enumerate(periodos.items()):
        with cols[idx]:
            if st.button(p, key=p, help=f"Visualizar dados de {p}", args=(p,), use_container_width=True):
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

    # Ajustar eixo Y automaticamente para não começar em zero
   
