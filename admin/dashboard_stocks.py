import streamlit as st
import pandas as pd

def dashboard_stocks():
    # Título ajustado com fonte sem negrito exagerado
    st.markdown("<h2 style='font-weight: 500;'>Ações Monitoradas</h2>", unsafe_allow_html=True)

    # Dados de exemplo (substituir pelos dados reais do banco)
    stocks = [
        ["ITSA4", "ITAUSA EJ", 8.84, 11.26, "9.08%", 11.20, "Industrials", "Dividends", "Teto $11.20"],
        ["VALE3", "VALE", 53.76, 56.00, "8.74%", 71.00, "Basic Materials", "Dividends", ""],
        ["BMGB4", "BANCO BMG", 3.73, 0.00, "12.65%", 0.00, "Financial Services", "Dividends", ""],
        ["RECR11", "FII REC", 74.10, 107.36, "10.67%", 98.22, "FII", "FII", "Papel"]
    ]

    df = pd.DataFrame(stocks, columns=["Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])

    # Ajuste de estilo para evitar quebra de linha
    styles = [
        dict(selector="th", props=[("text-align", "center"), ("font-weight", "bold"), ("background-color", "#333"), ("color", "white")]),
        dict(selector="td", props=[("text-align", "center"), ("white-space", "nowrap"), ("padding", "5px")]),
    ]

    # Alternância de cores entre linhas para melhor visualização
    def row_colors(row):
        return [
            "background-color: #2a2a2a; color: white;" if row.name % 2 == 0 else "background-color: #1f1f1f; color: white;"
        ] * len(row)

    st.table(df.style.apply(row_colors, axis=1).set_properties(**{'text-align': 'center'}))
