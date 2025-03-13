import streamlit as st
from auth.login import login
from admin.dashboard import admin_dashboard

# Inicializar sessão
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""

# Tela de login
if not st.session_state['logged_in']:
    login()

else:
    # Adiciona a barra lateral de navegação
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Admin"])

    if pagina == "Dashboard":
        st.write(f"📊 Bem-vindo, {st.session_state['user_email']}! Área do usuário em construção...")
    
    elif pagina == "Admin":
        if st.session_state['user_email'] == "jeisonmello@icloud.com":
            admin_dashboard()  # Apenas você acessa o painel administrativo
        else:
            st.error("❌ Acesso negado. Apenas administradores podem acessar esta área.")
