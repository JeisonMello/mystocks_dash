import streamlit as st
import yfinance as yf
import pandas as pd

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    try:
        # Buscar dados da ação
        stock = yf.Ticker(ticker)

        # Obter histórico de dividendos
        dividendos = stock.dividends
        historico = stock.history(period="10y")  # Histórico de preços para cálculo de dividend yield

        if dividendos.empty:
            st.warning("Nenhum histórico de dividendos encontrado para esta ação.")
        else:
            # Criar coluna de ano para agrupar os dividendos por ano
            dividendos = dividendos.reset_index()
            dividendos["Ano"] = dividendos["Date"].dt.year
            
            # Agrupar dividendos por ano
            dividendos_por_ano = dividendos.groupby("Ano")["Dividends"].sum().reset_index()
            
            # Calcular o preço médio anual da ação
            historico["Ano"] = historico.index.year
            preco_medio_anual = historico.groupby("Ano")["Close"].mean().reset_index()
            
            # Combinar dividendos com o preço médio da ação
            resultado = pd.merge(dividendos_por_ano, preco_medio_anual, on="Ano", how="left")
            resultado["Dividend Yield (%)"] = (resultado["Dividends"] / resultado["Close"]) * 100

            # Exibir resultados formatados
            st.write("**Histórico de Dividendos por Ano**")
            st.dataframe(resultado.rename(columns={"Ano": "Ano", "Dividends": "Dividendos Pagos", "Close": "Preço Médio", "Dividend Yield (%)": "Yield (%)"}))

    except Exception as e:
        st.error("Erro ao buscar dados da ação. Verifique o código e tente novamente.")
