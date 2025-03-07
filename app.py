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

        # ========================== 
        # PARTE 1: HISTÓRICO DE PREÇOS 
        # ========================== 
        st.markdown(f"<h2 style='color: white; font-size: 22px;'>{company_name} ({ticker})</h2>", unsafe_allow_html=True)

        # Preço atual e variação
        preco_atual = stock_info.get("regularMarketPrice", None)
        preco_anterior = stock_info.get("previousClose", None)

        if preco_atual and preco_anterior:
            variacao = preco_atual - preco_anterior
            porcentagem = (variacao / preco_anterior) * 100
            cor_variacao = "price-change-positive" if variacao > 0 else "price-change-negative"
            simbolo_variacao = "▲" if variacao > 0 else "▼"

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

        # Seletor de período funcional (SOMENTE PARA HISTÓRICO DE PREÇOS)
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

        # Atualizar dados conforme período selecionado (SOMENTE PARA PREÇOS)
        periodo = periodos[st.session_state["periodo_selecionado"]]
        dados_preco = stock.history(period=periodo)  

        # Gráfico de histórico de preços
        cor_grafico = "#34A853" if stock_info.get("regularMarketChange", 0) > 0 else "#EA4335"
        transparencia = "rgba(52, 168, 83, 0.2)" if stock_info.get("regularMarketChange", 0) > 0 else "rgba(234, 67, 53, 0.2)"

        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=dados_preco.index, 
            y=dados_preco["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color=cor_grafico, width=2),
            fillcolor=transparencia
        ))

        fig_price.update_layout(
            title="Histórico de Preços",
            xaxis_title="Data",
            yaxis_title=f"Preço ({moeda})",
            template="plotly_white"
        )

        st.plotly_chart(fig_price)

        # ========================== 
        # PARTE 2: HISTÓRICO DE DIVIDENDOS 
        # ========================== 
        st.subheader("Histórico de Dividendos")

        # Obter histórico de dividendos (NÃO TEM RELAÇÃO COM O GRÁFICO DE PREÇOS)
        dividendos = stock.dividends

        if dividendos.empty:
            st.warning("Nenhum histórico de dividendos encontrado para esta ação.")
        else:
            dividendos = dividendos.reset_index()
            dividendos["Ano"] = dividendos["Date"].dt.year
            dividendos_por_ano = dividendos.groupby("Ano")["Dividends"].sum().reset_index()

            # Criar gráfico de barras independente
            fig_dividendos = go.Figure()
            fig_dividendos.add_trace(go.Bar(
                x=dividendos_por_ano["Ano"],
                y=dividendos_por_ano["Dividends"],
                text=[f"{x:.2f}" for x in dividendos_por_ano["Dividends"]],
                textposition='auto',
                marker_color="#34A853"
            ))

            fig_dividendos.update_layout(
                title="Dividendos Pagos por Ano",
                xaxis_title="Ano",
                yaxis_title=f"Dividendos ({moeda})",
                template="plotly_dark"
            )

            st.plotly_chart(fig_dividendos)

            # Exibir tabela
            st.write("**Histórico de Dividendos por Ano**")
            st.dataframe(dividendos_por_ano.rename(columns={"Ano": "Ano", "Dividends": "Dividendos Pagos"}))

    except Exception as e:
        st.error("Ação não localizada, insira o código de uma ação existente.")
