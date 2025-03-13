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
        df = df.drop(columns=["ID"])  # Oculta a coluna ID para melhor visualização

        for i, row in df.iterrows():
            with st.expander(f"📌 {row['Papel']} - {row['Nome']}"):
                st.write(f"**Preço Atual:** R$ {row['Preço']:.2f}")
                st.write(f"**Yield:** {row['Yield']:.2f}%")
                st.write(f"**Custava:** R$ {row['Custava']:.2f}")
                st.write(f"**Preço Teto:** R$ {row['Preço Teto']:.2f}")
                st.write(f"**Setor:** {row['Setor']}")
                st.write(f"**Estratégia:** {row['Estratégia']}")
                st.write(f"**Observação:** {row['Observação']}")

                if st.button(f"✏️ Editar {row['Papel']}", key=f"edit_{row['Papel']}"):
                    st.session_state["edit_papel"] = row['Papel']
                    st.rerun()
    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Seção de remoção de ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
