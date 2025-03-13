import streamlit as st
import pandas as pd
import yfinance as yf
def debug_stock_data(papel):
    """Depuração: Exibir todas as informações retornadas pela API do Yahoo Finance"""
    papel_formatado = papel + ".SA"  # Formato correto para ações brasileiras
    stock = yf.Ticker(papel_formatado)
    info = stock.info  # Obtém todos os dados disponíveis

    st.subheader("🔍 Debug: Dados da API Yahoo Finance")
    st.json(info)  # Mostra todas as informações em formato JSON
from auth.database_stocks import add_stock, get_stocks, delete_stock, update_stock

def get_stock_data(papel):
    """Busca os dados da ação na API do Yahoo Finance."""
    try:
        papel_formatado = papel + ".SA"  # Yahoo Finance usa ".SA" para ações brasileiras
        stock = yf.Ticker(papel_formatado)
        info = stock.info

        # Captura o melhor valor disponível para yield de dividendos
        dividend_yield = info.get("trailingAnnualDividendYield", None)
        if dividend_yield is None:  # Se não existir, tenta o forwardDividendYield
            dividend_yield = info.get("forwardDividendYield", 0.0)

        return {
            "nome": " ".join(info.get("shortName", "Nome Desconhecido").split()[:2]),  # Mantém só os dois primeiros nomes
            "preco": round(info.get("regularMarketPrice", 0.0), 2),
            "yield": round(dividend_yield * 100, 2) if dividend_yield else 0.0,
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
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs."])
        df = df.drop(columns=["ID"])  # Oculta a coluna ID para melhor visualização

        # Formatar valores
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # Aplicar cores alternadas
        styled_df = df.style.set_properties(**{'text-align': 'center'})\
            .set_table_styles([{'selector': 'th', 'props': [('font-size', '16px'), ('text-align', 'center')]}])\
            .apply(lambda x: ['background-color: #333' if i % 2 == 0 else 'background-color: #222' for i in range(len(x))], axis=0)

        st.table(styled_df)
    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # Botão para exibir o formulário de adição
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
        estrategia = st.selectbox("Estratégia", ["Dividends", "Value Invest"])
        obs = st.text_input("Observação")

        if st.button("Adicionar Ação"):
            if papel and nome:
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
