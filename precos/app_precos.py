import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.title("Histórico de Dividendos 💰")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    try:
        # Buscar dados da ação
        stock = yf.Ticker(ticker)

        # ========================== 
        # HISTÓRICO DE DIVIDENDOS 
        # ========================== 
        st.subheader("Histórico de Dividendos")

        # Obter histórico de dividendos
        dividendos = stock.dividends
        historico = stock.history(period="10y")

        if dividendos.empty:
            st.warning("Nenhum histórico de dividendos encontrado para esta ação.")
        else:
            dividendos = dividendos.reset_index()
            dividendos["Ano"] = dividendos["Date"].dt.year
            dividendos_por_ano = dividendos.groupby("Ano")["Dividends"].sum().reset_index()

            historico["Ano"] = historico.index.year
            preco_medio_anual = historico.groupby("Ano")["Close"].mean().reset_index()

            resultado = pd.merge(dividendos_por_ano, preco_medio_anual, on="Ano", how="right")
            resultado["Dividend Yield (%)"] = (resultado["Dividends"] / resultado["Close"]) * 100
            resultado = resultado.fillna(0)

            resultado = resultado.sort_values(by="Ano", ascending=False).head(10).sort_values(by="Ano")

            fig_dividendos = go.Figure()
            fig_dividendos.add_trace(go.Bar(
                x=resultado["Ano"],
                y=resultado["Dividends"],
                text=[f"{x:.2f}" for x in resultado["Dividends"]],
                textposition='auto',
                marker_color="#34A853"
            ))

            fig_dividendos.update_layout(
                title="Dividendos Pagos por Ano",
                xaxis_title="Ano",
                yaxis_title="Dividendos (BRL)",
                template="plotly_dark"
            )

            st.plotly_chart(fig_dividendos)

            st.write("**Histórico de Dividendos por Ano**")
            st.dataframe(resultado.rename(columns={"Ano": "Ano", "Dividends": "Dividendos Pagos", "Close": "Preço Médio", "Dividend Yield (%)": "Yield (%)"}))

    except Exception as e:
        st.error("Ação não localizada, insira o código de uma ação existente.")
