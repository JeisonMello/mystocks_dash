import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock

def dashboard_stocks():
    st.markdown("<h1 style='font-size: 28px; font-weight: 500;'>Ações Monitoradas</h1>", unsafe_allow_html=True)

    # Buscar ações cadastradas no banco
    stocks = get_stocks()
    
    if stocks:
        # Garantir que os dados do banco tenham o mesmo número de colunas da tabela
        colunas = ["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"]
        df = pd.DataFrame(stocks, columns=colunas)

        # Remover a coluna ID (não é necessária na exibição)
        df.drop(columns=["ID"], inplace=True)

        # Criar botões clicáveis na coluna "Papel"
        df["Papel"] = df.apply(lambda row: f'<a href="#" onclick="window.location.search=\'?acao={row["Papel"]}\'" style="text-decoration: none; color: #1E88E5; font-weight: 600;">{row["Papel"]}</a>', axis=1)

        # Formatar números (duas casas decimais)
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # Exibir tabela corretamente formatada no Streamlit
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
    else:
        st.warning("Nenhuma ação cadastrada.")

    # Seção para adicionar ações
    with st.expander("➕ Adicionar Nova Ação"):
        st.subheader("Adicionar Nova Ação")
        papel = st.text_input("Papel (ex: CSMG3)").upper()
        custava = st.number_input("Custava", min_value=0.0, format="%.2f")
        preco_teto = st.number_input("Preço Teto", min_value=0.0, format="%.2f")
        estrategia = st.selectbox("Estratégia", ["Dividends", "Value Invest", "FII"])
        obs = st.text_input("Observação")

        if st.button("Adicionar Ação"):
            if papel:
                try:
                    stock_info = yf.Ticker(papel + ".SA").info
                    nome = stock_info.get("shortName", papel)
                    preco = stock_info.get("regularMarketPrice", 0.0)
                    setor = stock_info.get("sector", "Desconhecido")
                    yield_val = stock_info.get("trailingAnnualDividendYield", 0.0) * 100 if stock_info.get("trailingAnnualDividendYield") else 0.0

                    add_stock(papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs)
                    st.success(f"Ação {papel} adicionada com sucesso!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao buscar dados da ação: {e}")
            else:
                st.error("Digite um código de ação válido.")

    # Seção para remover ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
