import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock

def get_stock_data(papel):
    """Busca os dados da ação na API do Yahoo Finance."""
    try:
        papel_formatado = papel + ".SA"  # Yahoo Finance usa ".SA" para ações brasileiras
        stock = yf.Ticker(papel_formatado)
        info = stock.info

        return {
            "nome": info.get("shortName", "Nome Desconhecido"),
            "preco": info.get("regularMarketPrice", 0.0),
            "yield": round(info.get("trailingAnnualDividendYield", 0.0) * 100, 2) if info.get("trailingAnnualDividendYield") else 0.0,
            "setor": info.get("sector", "Setor Desconhecido")
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {papel}: {e}")
        return {"nome": "", "preco": 0.0, "yield": 0.0, "setor": ""}

def dashboard_stocks():
    st.title("Ações Monitoradas")

    # Obtém todas as ações cadastradas
    stocks = get_stocks()
    if stocks:
        # Criar DataFrame com as colunas organizadas corretamente
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # Remove a coluna de ID

        # Formatação dos valores numéricos
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")

        # Criar colunas com links clicáveis para abrir o gráfico
        df["Papel"] = df["Papel"].apply(lambda x: f'<a href="#" onclick="window.open(\'{x}\', \'_blank\')" style="color: #0d6efd; text-decoration: none;">{x}</a>')

        # Configurações de estilo para melhor exibição da tabela
        st.markdown(
            df.to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Adicionar nova ação
    with st.expander("➕ Adicionar Nova Ação"):
        st.subheader("Adicionar Nova Ação")
        papel = st.text_input("Papel (ex: CSMG3)").upper()

        if papel:
            stock_info = get_stock_data(papel)
            nome = stock_info["nome"]
            preco = stock_info["preco"]
            yield_val = stock_info["yield"]
            setor = stock_info["setor"]
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

    # Remover ações
    with st.expander("🗑️ Remover Ação"):
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir"):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
