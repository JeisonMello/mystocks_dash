import streamlit as st
import pandas as pd
import yfinance as yf
from auth.database_stocks import add_stock, get_stocks, delete_stock, update_stock

def get_stock_data(papel):
    """Busca os dados da ação na API do Yahoo Finance e formata corretamente."""
    try:
        papel_formatado = papel + ".SA"  # Yahoo Finance usa ".SA" para ações brasileiras
        stock = yf.Ticker(papel_formatado)
        info = stock.info

        # Obtendo os valores de dividend yield
        trailing_yield = info.get("trailingAnnualDividendYield", 0) or 0
        forward_yield = info.get("dividendYield", 0) or 0

        # Escolher o maior valor
        best_yield = max(trailing_yield, forward_yield)

        # **Correção**: Se o yield for maior que 1, ele já está em percentual e não deve ser multiplicado
        if best_yield > 1:
            best_yield = round(best_yield, 2)  # Apenas arredondar, sem multiplicação
        else:
            best_yield = round(best_yield * 100, 2)  # Multiplicar por 100 para percentual

        # Remover sufixos como ON, PN, etc.
        nome_limpo = " ".join(info.get("shortName", "Nome Desconhecido").split()[:2])

        return {
            "nome": nome_limpo,
            "preco": round(info.get("regularMarketPrice", 0.0), 2),
            "yield": best_yield,  # Agora sempre correto
            "setor": info.get("sector", "Setor Desconhecido")
        }
    except Exception as e:
        print(f"Erro ao buscar dados para {papel}: {e}")
        return {"nome": "", "preco": 0.0, "yield": 0.0, "setor": ""}

def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    # Exibir tabela de ações cadastradas de forma visualmente agradável
    stocks = get_stocks()
    if stocks:
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Nome", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # Oculta a coluna ID

        # Aplicando formatação
        df["Preço"] = df["Preço"].apply(lambda x: f"R$ {x:.2f}")
        df["Custava"] = df["Custava"].apply(lambda x: f"R$ {x:.2f}")
        df["Teto"] = df["Teto"].apply(lambda x: f"R$ {x:.2f}")
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")  # Agora correto

        # Exibir com estilo zebrado
        st.write(df.style.set_properties(**{'text-align': 'center'}).set_table_styles(
            [{'selector': 'thead th', 'props': [('background-color', '#333'), ('color', 'white'), ('font-weight', 'bold')]},
             {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#222')]}]
        ))
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
