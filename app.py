import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar os elementos ao estilo do Google Finance
st.markdown("""
    <style>
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
        hr {
            border: 0;
            height: 1px;
            background: #666;
            margin: 10px 0 10px 0;
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

    # Botões de período para histórico de preços
    periodos = {
        "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
        "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"
    }
    
    periodo_selecionado = "6M"  # Padrão: últimos 6 meses

    colunas = st.columns(len(periodos))
    for i, (label, value) in enumerate(periodos.items()):
        if colunas[i].button(label, key=f"btn_{label}"):
            periodo_selecionado = label  

    # Buscar histórico de preços da ação
    dados = stock.history(period=periodos[periodo_selecionado])

    # 📌 Exibir o preço da ação
    preco_atual = dados["Close"].iloc[-1]
    preco_anterior = dados["Close"].iloc[0]
    variacao = preco_atual - preco_anterior
    porcentagem = (variacao / preco_anterior) * 100
    cor_variacao = "#34A853" if variacao > 0 else "#EA4335"
    simbolo_variacao = "🔼" if variacao > 0 else "🔻"

    # Exibir preço da ação com variação percentual no topo
    st.markdown(f"""
    <h2 style='color:#ffffff; font-size: 28px;'>
        {preco_atual:.2f} BRL <span style='color:{cor_variacao}; font-size: 20px;'>
        {simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) nos últimos {periodo_selecionado}
    </span></h2>
    """, unsafe_allow_html=True)

    # Criar gráfico de preços
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#3454b4', width=2),
        fill='tozeroy',
        fillcolor='rgba(52, 84, 180, 0.2)'
    ))

    # Ajuste de escala para não encostar no zero
    min_preco = dados["Close"].min()
    max_preco = dados["Close"].max()
    margem = (max_preco - min_preco) * 0.1  

    fig_price.update_layout(
        template="plotly_dark",
        title=f"Evolução do Preço - {periodo_selecionado} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)", range=[min_preco - margem, max_preco + margem])
    )

    st.plotly_chart(fig_price)

    # 📌 Restaurando os Dividendos
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum().tail(10)

        preco_medio_anual = stock.history(period="10y")["Close"].resample("Y").mean()
        preco_medio_anual.index = preco_medio_anual.index.year
        preco_medio_anual = preco_medio_anual.reindex(dividendos.index, fill_value=1)
        dividend_yield = (dividendos / preco_medio_anual) * 100  

        dividend_yield = dividend_yield.replace([float("inf"), -float("inf")], 0).fillna(0)

        fig_divid = go.Figure()
        fig_divid.add_trace(go.Bar(
            x=dividend_yield.index,
            y=dividend_yield,
            text=dividend_yield.apply(lambda x: f"{x:.2f}%"),
            textposition='outside',
            marker=dict(color="#ad986e", opacity=0.8, line=dict(color="rgba(0, 0, 0, 0.3)", width=1)),
        ))

        fig_divid.update_layout(
            template="plotly_dark",
            title=f"Dividend Yield - Últimos 10 Anos ({ticker})",
            xaxis_title="Ano",
            yaxis_title="Yield (%)",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig_divid)
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
