import streamlit as st
import sys
import os

# Garantir que auth/ está no sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Testar importação do módulo `auth.login`
try:
    import auth.login  # Apenas testando a importação do módulo
    st.success("Módulo `auth.login` foi importado corretamente!")
except Exception as e:
    st.error(f"Erro ao importar `auth.login`: {e}")
    st.stop()
