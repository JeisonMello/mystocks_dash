import streamlit as st
from auth.database_stocks import add_stock, get_stocks, delete_stock

# Simulação de API para buscar dados
def get_stock_data(papel):
    """Simula uma API retornando dados do papel."""
    stock_data = {
        "CSMG3": {"nome": "Copasa", "preco": 22.83, "yield": 16.30, "setor": "Energia"},
        "PETR4": {"nome": "Petrobras", "preco": 30.45, "yield": 12.80, "setor": "Petróleo"},
        "VALE3": {"nome": "Vale", "preco": 68.50, "yield": 8.75, "setor": "Mineração"},
    }
    return stock_data.get(papel, {"nome": "", "preco": 0.0, "yield": 0.0, "setor": ""})

def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    # Exibir tabela de ações cadastradas
    stocks = get_stocks()
    if stocks:
        st.table(stocks)
    else:
        st.warning("Nenhuma ação cadastrada ainda.")

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

    st.subheader("Remover Ação")
    papel_excluir = st.text_input("Digite o código do papel para remover").upper()
    if st.button("Excluir"):
        delete_stock(papel_excluir)
        st.warning(f"Ação {papel_excluir} removida!")
        st.rerun()
