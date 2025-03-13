import streamlit as st
from auth.login import login
from admin.dashboard import admin_dashboard

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_email'] = ""  # Guarda o e-mail do usuário logado

if not st.session_state['logged_in']:
    login()
else:
    if st.session_state['user_email'] == "jeisonmello@icloud.com":
        admin_dashboard()  # Apenas você acessa o painel administrativo
    else:
        st.write(f"📊 Bem-vindo, {st.session_state['user_email']}! Área do usuário em construção...")
