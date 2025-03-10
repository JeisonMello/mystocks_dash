import streamlit as st
from auth.database import add_user, check_user

def login():
    st.title("Login")

    menu = ["Entrar", "Criar Conta"]
    escolha = st.selectbox("Escolha uma opção", menu)

    if escolha == "Entrar":
        email = st.text_input("E-mail")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if check_user(email, password):
                st.success(f"Bem-vindo, {email}!")
                st.session_state['logged_in'] = True
            else:
                st.error("E-mail ou senha incorretos.")

    elif escolha == "Criar Conta":
        new_email = st.text_input("E-mail")
        new_password = st.text_input("Escolha uma senha", type="password")
        confirm_password = st.text_input("Confirme sua senha", type="password")

        if st.button("Registrar"):
            if new_password != confirm_password:
                st.error("As senhas não coincidem!")
            elif add_user(new_email, new_password):
                st.success("Conta criada com sucesso! Agora você pode fazer login.")
            else:
                st.error("Erro ao criar conta. Esse e-mail já está cadastrado.")

if __name__ == "__main__":
    login()
