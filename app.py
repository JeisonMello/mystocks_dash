import streamlit as st
import sys
import os

# Garantir que o diretório base seja reconhecido
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth.login import login  # Importando diretamente a função login

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
