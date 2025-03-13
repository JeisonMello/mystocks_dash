import streamlit as st
from auth.login import login
from admin.dashboard import admin_dashboard

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Admin"])

    if pagina == "Dashboard":
        st.write("📊 Bem-vindo ao painel do usuário!")
    elif pagina == "Admin":
        admin_dashboard()
