import streamlit as st
import sys
import os

# Adiciona o diretório raiz ao caminho do Python
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from auth.login import login  # Importação padrão
except ModuleNotFoundError:
    st.error("Erro ao importar auth.login. Verifique o caminho e o nome dos arquivos.")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()  # Agora chamamos a função corretamente
else:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Histórico"])
    
    if pagina == "Dashboard":
        st.write("Aqui vai o código do Dashboard")
    elif pagina == "Histórico":
        st.write("Aqui vai o código do Histórico")
