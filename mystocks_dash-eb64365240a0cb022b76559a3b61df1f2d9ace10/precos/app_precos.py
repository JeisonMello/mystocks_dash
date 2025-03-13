import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import streamlit as st

def carregar_grafico_precos(ticker):
    """
    Busca os dados históricos de preços da ação e gera um gráfico interativo
    com opção de seleção de período e zoom dinâmico no gráfico.
    """

    try:
        # Ajusta o ticker para ações brasileiras
        if not ticker.endswith(".SA") and len(ticker) == 5:
            ticker += ".SA"

        stock = yf.Ticker(ticker)
        stock_info = stock.info

        if not stock_info or "longName" not in stock_info:
            return None, None

        company_name = stock_info.get("longName", ticker)
        moeda = stock_info.get("currency", "N/A")  
        preco_atual = stock_info.get("regularMarketPrice", None)
        preco_anterior = stock_info.get("previousClose", None)

        if preco_atual is None or preco_anterior is None:
            return None, None

        variacao = preco_atual - preco_anterior
        porcentagem = (variacao / preco_anterior) * 100
        cor_variacao = "price-change-positive" if variacao > 0 else "price-change-negative"
        simbolo_variacao = "▲" if variacao > 0 else "▼"

        horario_fechamento = stock_info.get("regularMarketTime", None)
        if horario_fechamento:
            from datetime import datetime
            horario = datetime.utcfromtimestamp(horario_fechamento).strftime('%d %b, %I:%M %p GMT-3')
            horario_texto = f"At close: {horario}"
        else:
            horario_texto = ""

        detalhes_acao = f"""
            <h2 style='color: white; font-size: 22px;'>{company_name} ({ticker})</h2>
            <div class="price-container">
                {preco_atual:.2f} {moeda} 
                <span class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%)</span>
            </div>
            <p class="timestamp">{horario_texto}</p>
        """

        # ==========================
        # SELETOR DE PERÍODO FUNCIONAL
        # ==========================
        periodos = {
            "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
            "YTD": "ytd", "1Y": "1y", "5Y": "5y", "ALL": "max"
        }

        if "periodo_selecionado" not in st.session_state:
            st.session_state["periodo_selecionado"] = "6M"

        colunas = st.columns(len(periodos))
        for i, (p, v) in enumerate(periodos.items()):
            with colunas[i]:
                if st.button(p, key=p):
                    st.session_state["periodo_selecionado"] = p

        periodo = periodos[st.session_state["periodo_selecionado"]]
        dados = stock.history(period=periodo)

        if dados.empty:
            return detalhes_acao, None

        cor_grafico = "#34A853" if variacao > 0 else "#EA4335"
        transparencia = "rgba(52, 168, 83, 0.2)" if variacao > 0 else "rgba(234, 67, 53, 0.2)"

        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color=cor_grafico, width=2),
            fillcolor=transparencia,
            hovertemplate=f'<b>%{{y:.2f}} {moeda}</b><br>%{{x|%d %b %y}}<extra></extra>'
        ))

        fig_price.update_layout(
            template="plotly_white",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            xaxis=dict(showgrid=False, range=[dados.index.min(), dados.index.max()]),
            yaxis=dict(range=[dados["Close"].min() * 0.95, dados["Close"].max() * 1.05],
                       showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)"),
            hoverlabel=dict(font_size=16)
        )

        return detalhes_acao, fig_price  

    except Exception as e:
        return None, None  
