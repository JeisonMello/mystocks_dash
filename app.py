import streamlit as st
from auth.login import login
from admin.dashboard_stocks import dashboard_stocks
from admin.dashboard import admin_dashboard

# Definição do estado de login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = None  # Armazena o e-mail do usuário logado

# Se não estiver logado, exibe a tela de login
if not st.session_state["logged_in"]:
    login()
else:
    # Layout com sidebar
    st.sidebar.title("Navegação")

    # Exibe o botão de Logout
    if st.sidebar.button("🚪 Sair"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None
        st.rerun()

    # Exibe opções de navegação de acordo com o usuário
    opcoes_paginas = ["Dashboard"]
    if st.session_state["user_email"] == "jeisonmello@icloud.com":  # Apenas o admin vê essa opção
        opcoes_paginas.append("Admin")

    pagina = st.sidebar.selectbox("Escolha uma página", opcoes_paginas)

    if pagina == "Dashboard":
        dashboard_stocks()
    elif pagina == "Admin":
        admin_dashboard()
