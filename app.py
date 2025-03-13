import streamlit as st
from auth.login import login
from admin.dashboard import admin_dashboard
from admin.dashboard_stocks import dashboard_stocks  # Agora temos os dois painéis

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Histórico", "Admin"])

    if pagina == "Dashboard":
        dashboard_stocks()  # Agora chama o Dashboard correto para ações
    elif pagina == "Histórico":
        st.write("Aqui vai o código do Histórico")
    elif pagina == "Admin":
        admin_dashboard()
