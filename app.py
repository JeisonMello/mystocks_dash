import streamlit as st
import auth.login  # Importamos o módulo

# Listar tudo o que existe dentro de `auth.login`
st.write("Conteúdo de auth.login:", dir(auth.login))
