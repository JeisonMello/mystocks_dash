import streamlit as st
import pandas as pd
from auth.database_stocks import get_stocks, add_stock, delete_stock

# Aplicar CSS para corrigir alinhamento e impedir quebras de linha
st.markdown(
    """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
            text-align: center;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        th {
            background-color: #333333;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #222222; /* Alternância de cor */
        }
        .botao-acao {
            text-decoration: none;
            font-weight: bold;
            color: #ffffff;
            background-color: #444444;
            padding: 6px 12px;
            border-radius: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .botao-acao:hover {
            background-color: #666666;
        }
        .botao-adicionar {
            background-color: #008000;
            color: white;
            padding: 8px 12px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .botao-adicionar:hover {
            background-color: #006400;
        }
        .botao-excluir {
            background-color: #800000;
            color: white;
            padding: 8px 12px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .botao-excluir:hover {
            background-color: #600000;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Função para exibir a tabela de ações
def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    stocks = get_stocks()
    
    if stocks:
        # Criar DataFrame
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df.drop(columns=["ID"], inplace=True)  # Removendo ID para exibição
        
        # Criar botões clicáveis dentro da tabela
        df["Papel"] = df["Papel"].apply(lambda x: f'<a href="?acao={x}" class="botao-acao">🔍 {x}</a>')
        
        # Exibir tabela com formatação correta
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.warning("Nenhuma ação cadastrada ainda.")

    # ---- Adicionar Nova Ação ----
    with st.expander("➕ Adicionar Nova Ação"):
        st.subheader("Adicionar Nova Ação")
        papel = st.text_input("Papel (ex: CSMG3)").upper()
        empresa = st.text_input("Empresa")
        preco = st.number_input("Preço Atual", min_value=0.0, format="%.2f")
        custava = st.number_input("Custava", min_value=0.0, format="%.2f")
        yield_val = st.number_input("Yield (%)", min_value=0.0, format="%.2f")
        preco_teto = st.number_input("Preço Teto", min_value=0.0, format="%.2f")
        setor = st.text_input("Setor")
        estrategia = st.selectbox("Estratégia", ["Dividends", "Value Invest", "FII"])
        obs = st.text_area("Observação")

        if st.button("Adicionar Ação", key="add", help="Adicionar nova ação", use_container_width=True):
            if papel and empresa:
                add_stock(papel, empresa, preco, custava, yield_val, preco_teto, setor, estrategia, obs)
                st.success(f"Ação {papel} adicionada com sucesso!")
                st.rerun()
            else:
                st.error("Por favor, insira um código de papel válido e o nome da empresa.")

    # ---- Remover Ação ----
    with st.expander("🗑️ Remover Ação"):
        st.subheader("Remover Ação")
        papel_excluir = st.text_input("Digite o código do papel para remover").upper()
        if st.button("Excluir", key="delete", help="Remover ação", use_container_width=True):
            delete_stock(papel_excluir)
            st.warning(f"Ação {papel_excluir} removida!")
            st.rerun()
