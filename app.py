import streamlit as st
import sys
import os

# Obtém o diretório base do projeto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Adiciona o diretório 'auth/' manualmente ao sys.path
AUTH_DIR = os.path.join(BASE_DIR, "auth")
if AUTH_DIR not in sys.path:
    sys.path.append(AUTH_DIR)

try:
    from login import login  # Agora importa diretamente da pasta auth/
    st.success("Importação de auth.login bem-sucedida!")
except ModuleNotFoundError as e:
    st.error(f"Erro ao importar login.py: {e}")

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
