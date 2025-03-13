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

    # Exibir tabela de ações cadastradas
    stocks = get_stocks()
    if stocks:
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Nome", "Preço", "Custava", "Yield", "Preço Teto", "Setor", "Estratégia", "Observação"])
        df = df.drop(columns=["ID"])  # Oculta a coluna ID
        for i, row in df.iterrows():
            with st.expander(f"📌 {row['Papel']} - {row['Nome']}"):
                st.write(f"**Preço Atual:** R$ {row['Preço']:.2f}")
                st.write(f"**Yield:** {row['Yield']:.2f}%")
                st.write(f"**Setor:** {row['Setor']}")
                st.write(f"**Estratégia:** {row['Estratégia']}")
                st.write(f"**Observação:** {row['Observação']}")

                # Botão para ativar edição
                if st.button(f"✏️ Editar {row['Papel']}", key=f"edit_{row['Papel']}"):
                    st.session_state["edit_papel"] = row['Papel']
                    st.rerun()

    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Seção de Edição
    if "edit_papel" in st.session_state:
        papel_editar = st.session_state["edit_papel"]
        st.subheader(f"✏️ Editando Ação: {papel_editar}")

        # Buscar os dados atuais para edição
        stock_atual = next((s for s in stocks if s[1] == papel_editar), None)
        if stock_atual:
            _, papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs = stock_atual

            novo_nome = st.text_input("Nome", nome)
            novo_preco = st.number_input("Preço Atual", value=preco, format="%.2f")
            novo_custava = st.number_input("Custava", value=custava, format="%.2f")
            novo_yield = st.number_input("Yield", value=yield_val, format="%.2f")
            novo_preco_teto = st.number_input("Preço Teto", value=preco_teto, format="%.2f")
            novo_setor = st.text_input("Setor", setor)
            nova_estrategia = st.selectbox("Estratégia", ["Dividends", "Value Invest"], index=["Dividends", "Value Invest"].index(estrategia))
            nova_obs = st.text_area("Observação", obs)

            if st.button("💾 Salvar Alterações"):
                resultado = update_stock(papel, novo_nome, novo_preco, novo_custava, novo_yield, novo_preco_teto, novo_setor, nova_estrategia, nova_obs)
                st.success(resultado)
                del st.session_state["edit_papel"]  # Remove o estado de edição
                st.rerun()

            if st.button("❌ Cancelar"):
                del st.session_state["edit_papel"]
                st.rerun()

    # Seção de remoção de ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
