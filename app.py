import sys
import os
import streamlit as st
from precos.app_precos import carregar_grafico_precos  # Importação correta

# 🛠 Adiciona o diretório raiz do projeto ao path do Python para encontrar módulos corretamente
sys.path.append(os.path.dirname(__file__))

# 🏆 Título do Dashboard
st.title("Dashboard de Ações 📈💰")

# 📌 Entrada do usuário para o ticker da ação
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker:
    # 🔹 Exibir Gráfico de Preços
    st.subheader("📊 Histórico de Preços")
    
    detalhes_acao, fig_precos = carregar_grafico_precos(ticker)  # Obtém os dados corretamente

    if detalhes_acao:
        st.markdown(detalhes_acao, unsafe_allow_html=True)  # Exibe detalhes formatados
    if fig_precos:
        st.plotly_chart(fig_precos)  # Exibe o gráfico
    else:
        st.error("Erro ao carregar o gráfico de preços. Verifique o código da ação e tente novamente.")
