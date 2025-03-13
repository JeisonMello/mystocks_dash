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

    # Opções padrão do menu
    opcoes_menu = ["Dashboard"]

    # Se for admin, adiciona a opção "Admin"
    if st.session_state['user_email'] == "jeisonmello@icloud.com":
        opcoes_menu.append("Admin")

    pagina = st.sidebar.selectbox("Escolha uma página", opcoes_menu)

    if pagina == "Dashboard":
        st.write(f"📊 Bem-vindo, {st.session_state['user_email']}! Área do usuário em construção...")
    
    elif pagina == "Admin":
        admin_dashboard()  # Exibe apenas para você (o admin)
