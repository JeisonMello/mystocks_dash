import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock, update_stock

def get_stock_data(papel):
    """Busca os dados da ação na API do Yahoo Finance."""
    try:
        papel_formatado = papel + ".SA"  # Yahoo Finance usa ".SA" para ações brasileiras
        stock = yf.Ticker(papel_formatado)
        info = stock.info

        return {
            "nome": info.get("shortName", "Nome Desconhecido"),
            "preco": info.get("regularMarketPrice", 0.0),
            "yield": info.get("trailingAnnualDividendYield", 0.0) * 100 if info.get("trailingAnnualDividendYield") else 0.0,
            "setor": info.get("sector", "Setor Desconhecido")
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {papel}: {e}")
        return {"nome": "", "preco": 0.0, "yield": 0.0, "setor": ""}

def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    stocks = get_stocks()
    if stocks:
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Nome", "Preço", "Custava", "Yield", "Preço Teto", "Setor", "Estratégia", "Observação"])
        df = df.drop(columns=["ID"])  # Oculta a coluna ID
        for i, row in df.iterrows():
            with st.expander(f"📌 {row['Papel']} - {row['Nome']}"):
                st.write(f"**Preço Atual:** R$ {row['Preço']:.2f}")
                st.write(f"**Yield:** {row['Yield']:.2f}%")
