import sys
import os
import streamlit as st
from precos.app_precos import carregar_grafico_precos

# 🛠 Adiciona o diretório raiz do projeto ao path do Python para encontrar módulos corretamente
sys.path.append(os.path.dirname(__file__))

# 🏆 Título do Dashboard
st.title("Dashboard de Ações 📈💰")

# 📌 Entrada do usuário para o ticker da ação
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker:
    # 🔹 Exibir Gráfico de Preços
    st.subheader("📊 Histórico de Preços")
    try:
        fig_precos = carregar_grafico_precos(ticker)
        st.plotly_chart(fig_precos)
    except Exception as e:
        st.error(f"Erro ao carregar gráfico de preços: {e}")
