import streamlit as st

def login():
    """Tela de login do sistema."""
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    
    if st.button("Entrar"):
        if validar_login(username, password):
            st.success(f"Bem-vindo, {username}!")
            return True
        else:
            st.error("Usuário ou senha incorretos")
    return False

def validar_login(username, password):
    """Função simples de validação de login (substituir por banco de dados futuramente)."""
    usuarios = {"admin": "1234", "user": "senha"}  # Exemplo simples
    return usuarios.get(username) == password

if __name__ == "__main__":
    login()
