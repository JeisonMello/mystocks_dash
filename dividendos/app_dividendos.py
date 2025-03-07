# Arquivo para histórico de dividendos
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

def carregar_grafico_dividendos(ticker):
    stock = yf.Ticker(ticker)
    dividendos = stock.dividends

    if dividendos.empty:
        return None, None  # Retorna vazio se não houver dividendos

    dividendos = dividendos.reset_index()
    dividendos["Ano"] = dividendos["Date"].dt.year
    dividendos_por_ano = dividendos.groupby("Ano")["Dividends"].sum().reset_index()

    # Criar range fixo de anos (últimos 10 anos)
    anos_referencia = list(range(datetime.now().year - 9, datetime.now().year + 1))
    dividendos_por_ano = dividendos_por_ano.set_index("Ano").reindex(anos_referencia, fill_value=0).reset_index()

    fig_dividendos = go.Figure()
    fig_dividendos.add_trace(go.Bar(
        x=dividendos_por_ano["Ano"],
        y=dividendos_por_ano["Dividends"],
        text=[f"{x:.2f}" for x in dividendos_por_ano["Dividends"]],
        textposition="auto",
        marker_color="#34A853"
    ))

    fig_dividendos.update_layout(
        title=f"Dividendos Pagos por Ano - {ticker}",
        xaxis_title="Ano",
        yaxis_title="Dividendos (BRL)",
        template="plotly_dark"
    )

    return fig_dividendos, dividendos_por_ano
