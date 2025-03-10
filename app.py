import streamlit as st
import auth.login as login  # Importa o módulo ao invés da função diretamente

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login.login()  # Agora chama login() dentro do módulo auth.login
else:
    st.sidebar.title("Navegação")
    pagina = st.sidebar.selectbox("Escolha uma página", ["Dashboard", "Histórico"])
    
    if pagina == "Dashboard":
        st.write("Aqui vai o código do Dashboard")
    elif pagina == "Histórico":
        st.write("Aqui vai o código do Histórico")
