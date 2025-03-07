# Arquivo para histórico de preços
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

def carregar_grafico_precos(ticker):
    stock = yf.Ticker(ticker)
    dados_preco = stock.history(period="1y")  # Pode mudar o período se quiser

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=dados_preco.index,
        y=dados_preco["Close"],
        mode="lines",
        line=dict(color="#34A853", width=2)
    ))

    fig_price.update_layout(
        title=f"Histórico de Preços - {ticker}",
        xaxis_title="Data",
        yaxis_title="Preço (BRL)",
        template="plotly_white"
    )

    return fig_price
