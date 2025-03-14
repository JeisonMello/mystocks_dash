import streamlit as st
import pandas as pd
from auth.database_stocks import get_stocks

# Aplicar CSS para corrigir a quebra de linha e melhorar a visualização
st.markdown(
    """
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            white-space: nowrap; /* Evita quebras de linha */
        }
        th {
            background-color: #333333;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #222222; /* Alternância de cor para facilitar leitura */
        }
        .botao-acao {
            text-decoration: none;
            font-weight: bold;
            color: #ffffff;
            background-color: #444444;
            padding: 6px 12px;
            border-radius: 5px;
            display: inline-block;
        }
        .botao-acao:hover {
            background-color: #666666;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Código para carregar as ações e exibir a tabela
def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    stocks = get_stocks()
    if stocks:
        # Criar DataFrame para exibição
        df = pd.DataFrame(stocks, columns=["Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])

        # Criar botões clicáveis para abrir detalhes da ação
        df["Papel"] = df["Papel"].apply(lambda x: f'<a href="?acao={x}" class="botao-acao">🔍 {x}</a>')

        # Exibir tabela formatada
        st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

    else:
        st.warning("Nenhuma ação cadastrada ainda.")
