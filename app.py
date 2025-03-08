import sys
import os
import streamlit as st

# 🛠 Adiciona o caminho do diretório do projeto ao sys.path para evitar erro de importação
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

try:
    from precos.app_precos import carregar_grafico_precos  # Importação correta
except ModuleNotFoundError as e:
    st.error(f"Erro ao importar módulo: {e}")
    st.stop()

# 🏆 Título do Dashboard
st.title("Dashboard de Ações 📈💰")

# 📌 Entrada do usuário para o ticker da ação
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker:
    st.subheader("📊 Histórico de Preços")

    try:
        detalhes_acao, fig_precos = carregar_grafico_precos(ticker)

        if detalhes_acao:
            st.markdown(detalhes_acao, unsafe_allow_html=True)
        if fig_precos:
            st.plotly_chart(fig_precos)
        else:
            st.error("❌ Nenhum dado de preço retornado. Verifique o código da ação.")

    except Exception as e:
        st.error(f"❌ Erro inesperado: {e}")
