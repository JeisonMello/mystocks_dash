import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

# Botões de período para histórico de preços
periodos = {"1D": "1d", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Máx": "max"}
periodo_escolhido = st.selectbox("Selecione o período:", list(periodos.keys()))

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period=periodos[periodo_escolhido])

    # Buscar preço atual e variação percentual
    preco_atual = dados["Close"].iloc[-1]
    preco_anterior = dados["Close"].iloc[0]
    variacao = preco_atual - preco_anterior
    porcentagem = (variacao / preco_anterior) * 100
    cor_variacao = "green" if variacao > 0 else "red"
    simbolo_variacao = "🔼" if variacao > 0 else "🔻"

    # Exibir valor atual e variação percentual no topo
    st.markdown(f"""
    <h2 style='color:{cor_variacao};'>
        {preco_atual:.2f} BRL {simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) nos últimos {periodo_escolhido}
    </h2>
    """, unsafe_allow_html=True)

    # 📌 Gráfico de Preços - Linha Azul Royal, com Suavização
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
        title=f"Evolução do Preço - {periodo_escolhido} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255, 255, 255, 0.2)", range=[min_preco - margem, max_preco + margem])  # Ajuste da proporção correta
    )

    st.plotly_chart(fig_price)

    # 📌 Gráfico de Dividendos - Últimos 10 Anos
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum()

        # 📌 Pegando os últimos 10 anos corretamente
        dividendos = dividendos.tail(10)

        # 📌 Calcular o percentual de dividendos em relação ao preço médio do ano
        preco_medio_anual = stock.history(period="10y")["Close"].resample("Y").mean()
        preco_medio_anual.index = preco_medio_anual.index.year
        preco_medio_anual = preco_medio_anual.reindex(dividendos.index, fill_value=1)
        dividend_yield = (dividendos / preco_medio_anual) * 100  # Em %

        # ✅ Remover valores NaN e infinitos
        dividend_yield = dividend_yield.replace([float("inf"), -float("inf")], 0).fillna(0)

        # Criar gráfico estilizado
        fig_divid = go.Figure()

        fig_divid.add_trace(go.Bar(
            x=dividend_yield.index,  # Pegando os anos corretos
            y=dividend_yield,
            text=dividend_yield.apply(lambda x: f"{x:.2f}%"),  # Exibir % diretamente nas barras
            textposition='outside',
            marker=dict(
                color="#ad986e",  # Barras douradas
                opacity=0.8,  # Suavização na cor
                line=dict(color="rgba(0, 0, 0, 0.3)", width=1),  # Contorno sutil
            )
        ))

        fig_divid.update_layout(
            template="plotly_dark",
            title=f"Dividend Yield - Últimos 10 Anos ({ticker})",
            xaxis_title="Ano",
            yaxis_title="Yield (%)",
            margin=dict(l=40, r=40, t=40, b=40)
        )

        st.plotly_chart(fig_divid)

        # 📌 Estatísticas de Dividendos
        st.subheader(f"📊 Estatísticas de Dividendos - {ticker}")
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_10_anos = dividendos.mean()  # Agora pega só os últimos 10 anos
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f} ({dividend_yield.iloc[-1]:.2f}%)")
        st.write(f"🔹 **Média dos últimos 10 anos:** {media_10_anos:.2f}")
        
        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write(f"✅ **{ticker} pagou dividendos em todos os últimos 10 anos.**")
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
