import streamlit as st
from auth.database import add_user, check_user

def login():
    st.title("Login")

    menu = ["Entrar", "Criar Conta"]
    escolha = st.selectbox("Escolha uma opção", menu)

    if escolha == "Entrar":
        username = st.text_input("Usuário")
        password = st.text_input("Senha", type="password")

        if st.button("Entrar"):
            if check_user(username, password):
                st.success(f"Bem-vindo, {username}!")
                st.session_state['logged_in'] = True
            else:
                st.error("Usuário ou senha incorretos.")

    elif escolha == "Criar Conta":
        new_username = st.text_input("Novo Usuário")
        new_password = st.text_input("Nova Senha", type="password")
        if st.button("Registrar"):
            if add_user(new_username, new_password):
                st.success("Usuário criado com sucesso! Agora você pode fazer login.")
            else:
                st.error("Erro ao criar usuário. Tente outro nome.")

if __name__ == "__main__":
    login()
