import streamlit as st
import sys
import os

# Adiciona manualmente auth ao sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from auth import login  # Apenas teste de importação
    st.success("Importação bem-sucedida!")
except Exception as e:
    st.error(f"Erro na importação: {e}")
    st.stop()
