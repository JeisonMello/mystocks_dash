import streamlit as st
import pandas as pd
from auth.database_stocks import get_stocks

# Aplicar CSS para corrigir a quebra de linha
st.markdown(
    """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            white-space: nowrap; /* Evita quebras de linha */
        }
        th {
            background-color: #333333;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #222222; /* Alternância de cor para facilitar leitura */
        }
    </style>
    """,
    unsafe_allow_html=True

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
            <a href="?stock={papel}" style="text-decoration:none; color:white; font-weight:bold; display:inline-flex; align-items:center; gap:5px; white-space:nowrap;">
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

    # **Seção para adicionar nova ação**
    with st.expander("➕ Adicionar Nova Ação"):
        st.subheader("Adicionar Nova Ação")
        papel = st.text_input("Papel (ex: CSMG3)").upper()
        empresa = st.text_input("Nome da Empresa")
        preco = st.number_input("Preço", min_value=0.0, format="%.2f")
        custava = st.number_input("Custava", min_value=0.0, format="%.2f")
        teto = st.number_input("Teto", min_value=0.0, format="%.2f")
        setor = st.text_input("Setor")
        estrategia = st.selectbox("Estratégia", ["Dividends", "FII", "Value Invest"])
        obs = st.text_input("Observação")

        if st.button("Adicionar Ação"):
            add_stock(papel, empresa, preco, custava, 0.0, teto, setor, estrategia, obs)
            st.success(f"Ação {papel} adicionada com sucesso!")
            st.rerun()

    # **Seção para remover ação**
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
