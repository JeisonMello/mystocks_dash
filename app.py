import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from yahooquery import search  # Corrigido: Importação correta para busca automática

# Estilização CSS para alinhar com o Google Finance
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
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("Dashboard da Ação")

# ==============================
# 🔍 BUSCA AUTOMÁTICA DE EMPRESAS
# ==============================
st.subheader("🔎 Buscar empresa listada")

ticker_input = st.text_input("Digite o nome ou código da ação:")

# Quando o usuário digita, buscamos empresas relacionadas
if ticker_input:
    try:
        # Fazer a busca no Yahoo Finance
        resultados = search(ticker_input)

        # Verifica se encontrou algo
        if "quotes" in resultados and resultados["quotes"]:
            opcoes = {r["symbol"]: r["shortname"] for r in resultados["quotes"]}
            escolha = st.selectbox("Selecione a empresa:", list(opcoes.values()), index=0)
            
            # Encontrar o ticker correspondente
            ticker = [k for k, v in opcoes.items() if v == escolha][0]
        else:
            st.error("❌ Nenhuma empresa encontrada. Tente outro nome ou código.")
            ticker = None
    except Exception as e:
        st.error(f"❌ Erro ao buscar empresas: {str(e)}")
        ticker = None
else:
    ticker = None

# Se tivermos um ticker válido, continuar com a busca de dados
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
