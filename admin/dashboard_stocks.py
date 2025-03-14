import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock, update_stock

def get_stock_data(papel):
    """Busca os dados da ação na API do Yahoo Finance e formata corretamente."""
    try:
        papel_formatado = papel + ".SA"
        stock = yf.Ticker(papel_formatado)
        info = stock.info

        # Obtendo o Yield correto
        trailing_yield = info.get("trailingAnnualDividendYield", 0) or 0
        forward_yield = info.get("dividendYield", 0) or 0
        best_yield = max(trailing_yield, forward_yield)
        best_yield = round(best_yield * 100, 2) if best_yield <= 1 else round(best_yield, 2)

        # Limpar o nome da empresa, removendo ON, PN, etc.
        nome_limpo = " ".join(info.get("shortName", "Nome Desconhecido").split()[:2])

        return {
            "nome": nome_limpo,
            "preco": round(info.get("regularMarketPrice", 0.0), 2),
            "yield": best_yield,
            "setor": info.get("sector", "Setor Desconhecido")
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {papel}: {e}")
        return {"nome": "", "preco": 0.0, "yield": 0.0, "setor": ""}

def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    # Buscar ações cadastradas
    stocks = get_stocks()
    if stocks:
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # **Ocultar a coluna de ID**

        # Aplicando formatação correta
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")

        # **Detectando o tema atual do Streamlit (claro ou escuro)**
        theme = st.get_option("theme.base")  # Retorna "light" ou "dark"
        bg_color = "#f5f5f5" if theme == "light" else "#333"  # Cinza claro no modo claro, cinza escuro no modo escuro
        text_color = "#000" if theme == "light" else "#FFF"  # Preto no modo claro, branco no modo escuro

        # **Aplicando Estilo com cores alternadas**
        def apply_row_style(index):
            return f'background-color: {bg_color}; color: {text_color}' if index % 2 == 1 else ''

        styled_df = df.style.apply(lambda row: [apply_row_style(row.name)] * len(row), axis=1).set_table_styles([
            {'selector': 'thead th', 'props': [('background-color', '#222'), ('color', 'white'), ('font-weight', 'bold'), ('text-align', 'center')]},
            {'selector': 'td', 'props': [('padding', '10px'), ('text-align', 'center')]}  # Melhor espaçamento e alinhamento
        ])

        st.write(styled_df, unsafe_allow_html=True)  # **Renderiza a tabela com estilo**
        
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
