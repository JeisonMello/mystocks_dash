import streamlit as st
from auth.database import add_user, check_email_exists

def login():
    """Tela de login do sistema."""
    st.title("Login")

    menu = ["Entrar", "Criar Conta"]
    escolha = st.selectbox("Escolha uma opção", menu)

    if escolha == "Entrar":
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            st.session_state['logged_in'] = True
            st.success(f"Bem-vindo, {email}!")
            st.rerun()

    elif escolha == "Criar Conta":
        new_email = st.text_input("E-mail")
        new_password = st.text_input("Escolha uma senha", type="password")
        confirm_password = st.text_input("Confirme sua senha", type="password")

        if st.button("Registrar"):
            if new_password != confirm_password:
                st.error("As senhas não coincidem!")
            else:
                resultado = add_user(new_email, new_password)
                if resultado == "success":
                    st.success("Conta criada com sucesso! Redirecionando para o login...")
                    st.rerun()
                else:
                    st.error("Erro ao criar conta. Esse e-mail já está cadastrado.")
