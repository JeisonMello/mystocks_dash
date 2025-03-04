import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar os elementos ao estilo do Google Finance
st.markdown("""
    <style>
        /* Estilização dos botões de período */
        div[data-testid="stButton"] > button {
            background-color: transparent !important;
            border: none !important;
            color: #cccccc !important;
            font-size: 16px !important;
            font-weight: normal !important;
            padding: 6px 15px !important;
            text-transform: none !important;
        }
        div[data-testid="stButton"] > button:hover {
            color: #ffffff !important;
            border-bottom: 2px solid #4285F4 !important;
        }
        div[data-testid="stButton"] > button:focus {
            color: #4285F4 !important;
            border-bottom: 2px solid #4285F4 !important;
        }
        /* Linha separadora sutil */
        hr {
            border: 0;
            height: 1px;
            background: #666;
            margin: 10px 0 10px 0;
        }
        /* Estilização do preço da ação */
        .stock-price {
            font-size: 36px;
            font-weight: bold;
            color: #ffffff;
        }
        .price-variation {
            font-size: 20px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)

    # 📌 Adicionar uma linha separadora antes dos botões de período
    st.markdown("<hr>", unsafe_allow_html=True)

    # Botões de período para histórico de preços (agora só aparecem após selecionar a ação)
    periodos = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"}
    periodo_selecionado = "6M"  # Sempre começa com 6 meses por padrão

    colunas = st.columns(len(periodos))
    for i, (label, value) in enumerate(periodos.items()):
        if colunas[i].button(label, key=f"btn_{label}"):
            periodo_selecionado = label  # Atualiza o período quando um botão é clicado

    # Buscar histórico de preços da ação com base no período selecionado
    dados = stock.history(period=periodos[periodo_selecionado])

    # 📌 Exibir o preço da ação
    preco_atual = dados["Close"].iloc[-1]
    preco_anterior = dados["Close"].iloc[0]
    variacao = preco_atual - preco_anterior
    porcentagem = (variacao / preco_anterior) * 100
    cor_variacao = "#34A853" if variacao > 0 else "#EA4335"  # Verde para alta, vermelho para queda
    simbolo_variacao = "🔼" if variacao > 0 else "🔻"

    # Exibir preço da ação com variação percentual no topo, formatado corretamente
    st.markdown(f"""
    <p class="stock-price">{preco_atual:.2f} BRL</p>
    <p class="price-variation" style="color:{cor_variacao};">
        {simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) nos últimos {periodo_selecionado}
    </p>
    """, unsafe_allow_html=True)

    # Criar gráfico de preços
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#3454b4', width=2),  # Azul royal claro, mais fino e elegante
        fill='tozeroy',
        fillcolor='rgba(52, 84, 180, 0.2)'  # Transparência suave no fundo
    ))

    # Ajuste na escala para não encostar no zero
    min_preco = dados["Close"].min()
    max_preco = dados["Close"].max()
    margem = (max_preco - min_preco) * 0.1  # Adiciona uma margem de 10%

    fig_price.update_layout(
        template="plotly_dark",
        title=f"Evolução do Preço - {periodo_selecionado} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)", range=[min_preco - margem, max_preco + margem])  # Ajuste da proporção correta
    )

    st.plotly_chart(fig_price)
