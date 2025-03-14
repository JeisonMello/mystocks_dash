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

        # Aplicar formatação de valores numéricos com 2 casas decimais
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # Criar links com botão interativo dentro da célula da coluna "Papel"
        df["Papel"] = df["Papel"].apply(lambda papel: f'''
            <a href="?stock={papel}" style="text-decoration:none; color:white; font-weight:bold; display:inline-flex; align-items:center; gap:5px;">
                <span>🔍</span> <span>{papel}</span>
            </a>
        ''')

        # Exibir a tabela formatada corretamente
        st.markdown(
            df.to_html(escape=False, index=False, justify='center', border=0).replace("\\n", ""),
            unsafe_allow_html=True
        )

    else:
        st.warning("Nenhuma ação cadastrada ainda.")
