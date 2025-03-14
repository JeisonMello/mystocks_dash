import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock, update_stock

def dashboard_stocks():
    st.markdown("<h1 style='font-size:36px; font-weight:400;'>Ações Monitoradas</h1>", unsafe_allow_html=True)

    # Obtém as ações cadastradas
    stocks = get_stocks()
    if stocks:
        # Criando DataFrame
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # Oculta o ID
        
        # Ajusta a formatação dos valores
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        
        # Cria os links dos papéis para abrir o dashboard individual
        df["Papel"] = df.apply(lambda row: f"<a href='?papel={row['Papel']}' target='_self' style='color: #1f77b4; text-decoration: none;'>{row['Papel']}</a>", axis=1)

        # Exibe a tabela formatada com rolagem horizontal para evitar quebras
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Botão para adicionar ação
    with st.expander("➕ Adicionar Nova Ação"):
        st.subheader("Adicionar Nova Ação")
        papel = st.text_input("Papel (ex: CSMG3)").upper()
        
        if papel:
            stock_info = yf.Ticker(papel + ".SA").info
            nome = stock_info.get("shortName", "Nome Desconhecido")
            preco = stock_info.get("regularMarketPrice", 0.0)
            yield_val = stock_info.get("trailingAnnualDividendYield", 0.0) * 100 if stock_info.get("trailingAnnualDividendYield") else 0.0
            setor = stock_info.get("sector", "Setor Desconhecido")
        else:
            nome, preco, yield_val, setor = "", 0.0, 0.0, ""

        custava = st.number_input("Custava", min_value=0.0, format="%.2f")
        preco_teto = st.number_input("Preço Teto", min_value=0.0, format="%.2f")
        estrategia = st.selectbox("Estratégia", ["Dividends", "Value Invest", "FII"])
        obs = st.text_input("Observação")

        if st.button("Adicionar Ação"):
            if papel and nome and preco > 0:
                add_stock(papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs)
                st.success(f"Ação {papel} adicionada com sucesso!")
                st.rerun()
            else:
                st.error("Papel inválido ou não encontrado na API.")

    # Seção de remoção de ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
