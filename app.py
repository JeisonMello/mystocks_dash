import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from yahooquery import search  # Importação correta para busca automática

# Estilização CSS para alinhar com o Google Finance
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        
        body {
            font-family: 'Inter', sans-serif;
        }
        .suggestion-box {
            margin-top: 5px;
            background: #222;
            padding: 5px;
            border-radius: 5px;
        }
        .suggestion {
            color: white;
            cursor: pointer;
            padding: 5px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .suggestion:hover {
            background: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("Dashboard da Ação")

# ==============================
# 🔍 BUSCA AUTOMÁTICA DE EMPRESAS SEM DUPLICAÇÃO
# ==============================
st.subheader("🔎 Buscar empresa listada")

# Campo de entrada para buscar empresas
ticker_input = st.text_input("Digite o nome ou código da ação:")

# Inicializando a variável do ticker
ticker = None
opcoes = {}

# Buscar sugestões ao digitar
if ticker_input:
    try:
        resultados = search(ticker_input)  # Faz a busca de ações no Yahoo Finance

        if "quotes" in resultados and resultados["quotes"]:
            # Criar dicionário {Ticker: Nome da Empresa}
            opcoes = {r["symbol"]: f"{r['shortname']} ({r['symbol']})" for r in resultados["quotes"]}

            # Exibir sugestões abaixo do campo de entrada como botões
            st.markdown('<div class="suggestion-box">', unsafe_allow_html=True)
            for k, v in opcoes.items():
                if st.button(v, key=k):
                    ticker = k  # Quando o usuário clica, selecionamos esse ticker
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("❌ Nenhuma empresa encontrada. Tente outro nome ou código.")
    except Exception as e:
        st.error(f"❌ Erro ao buscar empresas: {str(e)}")

# Se um ticker foi selecionado, continuamos com os dados
if ticker:
    try:
        stock = yf.Ticker(ticker)
        stock_info = stock.info  

        if "longName" not in stock_info:
            st.error("❌ Ação não encontrada! Verifique o código e tente novamente.")
        else:
            company_name = stock_info.get("longName", ticker)
            setor_en = stock_info.get("sector", "Setor não disponível")

            st.subheader(company_name)
            st.markdown(f'<div class="sector-text">Setor: {setor_en}</div>', unsafe_allow_html=True)

            # ==========================
            # HISTÓRICO DE PREÇOS
            # ==========================
            st.subheader("Histórico de Preços")

            periodos = {
                "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
                "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"
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

            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=dados.index, 
                y=dados["Close"], 
                mode='lines',
                line=dict(color='#4285F4', width=2),
                fill='tozeroy',
                fillcolor='rgba(66, 133, 244, 0.2)'  
            ))

            min_price = dados["Close"].min()
            max_price = dados["Close"].max()
            fig_price.update_layout(
                template="plotly_dark",
                xaxis_title="",
                yaxis_title="Preço (R$)",
                margin=dict(l=40, r=40, t=40, b=40),
                font=dict(color="white"),
                xaxis=dict(showgrid=False),
                yaxis=dict(range=[min_price * 0.98, max_price * 1.02],
                        showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)"),
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig_price)

    except Exception as e:
        st.error(f"❌ Erro ao buscar os dados da ação: {str(e)}")
