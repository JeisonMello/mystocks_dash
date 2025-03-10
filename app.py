import streamlit as st
import sys
import os

# Depuração: Mostrar diretórios acessíveis no Streamlit
st.write("Diretórios disponíveis:", sys.path)

try:
    from auth.login import login  # Importação padrão
    st.success("Importação de auth.login bem-sucedida!")
except ModuleNotFoundError as e:
    st.error(f"Erro ao importar auth.login: {e}")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Histórico"])
    
    if pagina == "Dashboard":
        st.write("Aqui vai o código do Dashboard")
    elif pagina == "Histórico":
        st.write("Aqui vai o código do Histórico")
