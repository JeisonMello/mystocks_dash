import streamlit as st
from auth.login import login
from admin.dashboard_stocks import dashboard_stocks
from admin.dashboard import admin_dashboard

# Função para salvar login nos parâmetros da URL
def save_login_state(email):
    st.experimental_set_query_params(user_email=email)

# Função para carregar login da URL, se disponível
def load_login_state():
    query_params = st.experimental_get_query_params()
    return query_params.get("user_email", [None])[0]

# Se o estado de login não estiver definido, carregamos dos parâmetros
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = load_login_state()

# Se não estiver logado, exibe a tela de login
if not st.session_state["logged_in"]:
    login()
else:
    # Se houver um e-mail salvo, consideramos o usuário logado
    if st.session_state["user_email"]:
        st.session_state["logged_in"] = True

    # Sidebar de navegação
    st.sidebar.title("Navegação")

    # Exibe botão de Logout
    if st.sidebar.button("🚪 Sair"):
        st.session_state["logged_in"] = False
        st.session_state["user_email"] = None
        st.experimental_set_query_params()  # Limpa os parâmetros de login da URL
        st.rerun()

    # Define as opções disponíveis para navegação
    opcoes_paginas = ["Dashboard"]
    if st.session_state["user_email"] == "jeisonmello@icloud.com":  # Apenas admin vê Admin
        opcoes_paginas.append("Admin")

    pagina = st.sidebar.selectbox("Escolha uma página", opcoes_paginas)

    if pagina == "Dashboard":
        dashboard_stocks()
    elif pagina == "Admin":
        admin_dashboard()
