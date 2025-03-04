import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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
    dados = stock.history(period="10y")

    # Buscar setor da empresa
    setor = stock.info.get("sector", "Setor não encontrado")
    st.subheader(f"🏢 Setor da Empresa - {ticker}")
    st.write(f"📌 **{setor}**")

    # 📌 Gráfico de Preços Mantendo Cores Originais
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()
    
    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        fill='tozeroy',
        line=dict(color='#3454b4', width=3),  # Azul original
        fillcolor='rgba(52, 84, 180, 0.3)'  # Transparência azul suave
    ))

    fig_price.update_layout(
        template="plotly_dark",
        title=f"Evolução do Preço - {ticker}",
        xaxis_title="Ano",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig_price)

    # 📌 Gráfico de Dividendos - Ajustado para 10 anos e cores mantidas
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum()

        # 📌 Pegando os últimos 10 anos corretamente
        dividendos = dividendos.tail(10)

        # 📌 Calcular o percentual de dividendos em relação ao preço médio do ano
        preco_medio_anual = dados["Close"].resample("Y").mean()
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
