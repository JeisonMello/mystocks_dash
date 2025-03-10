
import streamlit as st
from auth.database import delete_user

def admin_dashboard():
    """Painel de Administração"""
    st.title("🔧 Painel de Administração")

    # Controle de Administradores
    admins = ["jeisonmello@icloud.com"]  # Lista de admins permitidos

    if "admin_logged" not in st.session_state:
        st.session_state["admin_logged"] = False

    email_admin = st.text_input("Digite seu e-mail de admin")
    if st.button("Entrar como Admin"):
        if email_admin in admins:
            st.session_state["admin_logged"] = True
            st.success("Login de administrador bem-sucedido!")
            st.rerun()
        else:
            st.error("Acesso negado! Apenas administradores podem acessar.")

    if st.session_state["admin_logged"]:
        st.subheader("⚠️ Remover Conta (Apenas para Admins)")
        email_delete = st.text_input("Digite o e-mail para remover")
        if st.button("Excluir Usuário"):
            resultado = delete_user(email_delete)
            st.warning(resultado)
            st.rerun()

        st.subheader("📌 Mais funcionalidades podem ser adicionadas aqui futuramente!")
