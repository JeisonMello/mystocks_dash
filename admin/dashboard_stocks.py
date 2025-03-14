import streamlit as st
import pandas as pd
from auth.database_stocks import get_stocks, delete_stock, add_stock

def dashboard_stocks():
    st.markdown("<h2 style='font-weight: normal;'>Ações Monitoradas</h2>", unsafe_allow_html=True)

    # Buscar ações cadastradas
    stocks = get_stocks()

    if stocks:
        # Criar DataFrame verificando a estrutura dos dados
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        
        # Remover a coluna "ID" que não precisa ser mostrada
        df = df.drop(columns=["ID"])

        # Formatar colunas numéricas
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # Aplicar estilos corretos para manter o layout igual ao do anexo 02
        styled_df = df.style.set_properties(**{
            "text-align": "center",
            "white-space": "nowrap",
        }).set_table_styles([
            {"selector": "th", "props": [("font-weight", "bold"), ("text-align", "center"), ("padding", "5px")]}
        ])

        st.dataframe(styled_df, use_container_width=True)

    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Formulário para adicionar ações
    with st.expander("➕ Adicionar Nova Ação"):
        papel = st.text_input("Papel (ex: CSMG3)").upper()
        nome = st.text_input("Nome da Empresa")
        preco = st.number_input("Preço Atual", format="%.2f")
        custava = st.number_input("Custava", format="%.2f")
        preco_teto = st.number_input("Preço Teto", format="%.2f")
        estrategia = st.selectbox("Estratégia", ["Dividends", "FII", "Value Invest"])
        obs = st.text_area("Observação")

        if st.button("Adicionar Ação"):
            add_stock(papel, nome, preco, custava, preco_teto, estrategia, obs)
            st.success(f"Ação {papel} adicionada com sucesso!")
            st.rerun()

    # Seção de remoção de ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
