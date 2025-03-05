import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar com o Google Finance
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
        }
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
st.title("📊 Dashboard da Ação")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")

    # Buscar setor da empresa
    setor = stock.info.get("sector", "Setor não encontrado")
    st.subheader(f"🏢 Setor da Empresa - {ticker}")
    st.write(f"📌 {setor}")

    # =====================================
    # 📌 PARTE 01 - HISTÓRICO DE PREÇOS
    # =====================================
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    
    # Botões de período
    periodos = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"}
    periodo_selecionado = st.radio("Escolha o período:", list(periodos.keys()), index=3, horizontal=True)
    periodo = periodos[periodo_selecionado]
    
    # Atualizar os dados com base no período
    dados = stock.history(period=periodo)

    # Criar gráfico no estilo Google Finance
    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#4285F4', width=2)
    ))
    
    fig_price.update_layout(
        template="plotly_white",
        xaxis_title="",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        font=dict(color="white"),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig_price)

    # =====================================
    # 📌 PARTE 02 - DIVIDENDOS ANUAIS
    # =====================================

    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum().tail(10)
        anos = dividendos.index.year
        
        fig_divid = go.Figure()
        fig_divid.add_trace(go.Bar(
            x=anos,
            y=dividendos,
            text=dividendos.apply(lambda x: f"{x:.2f}"),
            textposition='outside',
            marker=dict(color="#ad986e", opacity=0.8, line=dict(color="rgba(0, 0, 0, 0.3)", width=1)),
        ))

        fig_divid.update_layout(
            template="plotly_dark",
            title=f"Dividend Yield - Últimos 10 Anos ({ticker})",
            xaxis_title="Ano",
            yaxis_title="Dividendos (R$)",
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(color="white")
        )

        st.plotly_chart(fig_divid)

        # 📌 Estatísticas de Dividendos
        st.subheader(f"📊 Estatísticas de Dividendos - {ticker}")
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_10_anos = dividendos.mean()
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f}")
        st.write(f"🔹 **Média dos últimos 10 anos:** {media_10_anos:.2f}")

        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write(f"✅ **{ticker} pagou dividendos em todos os últimos 10 anos.**")
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
