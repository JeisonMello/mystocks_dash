import streamlit as st
import pandas as pd
import yfinance as yf

from auth.database_stocks import get_stocks

def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    # Obter as ações cadastradas
    stocks = get_stocks()

    if stocks:
        # Criar um DataFrame com os dados formatados corretamente
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # Remover a coluna ID

        # Aplicar duas casas decimais a valores numéricos
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # Criar botões interativos dentro da tabela para cada papel (HTML + JS)
        df["Papel"] = df["Papel"].apply(lambda papel: f'''
            <a href="?stock={papel}" style="text-decoration:none; color:white; font-weight:bold; display:flex; align-items:center;">
                <span style="margin-right:5px;">🔍</span> {papel}
            </a>
        ''')

        # Exibir a tabela formatada corretamente sem quebras de linha
        st.markdown(
            df.to_html(escape=False, index=False, justify='center', border=0),
            unsafe_allow_html=True
        )

    else:
        st.warning("Nenhuma ação cadastrada ainda.")
