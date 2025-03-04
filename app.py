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
    dados = stock.history(period="6mo")  # Últimos 6 meses

    # Buscar preço atual e variação do dia
    preco_atual = dados["Close"].iloc[-1]
    variacao = preco_atual - dados["Close"].iloc[-2]
    porcentagem = (variacao / dados["Close"].iloc[-2]) * 100
    cor_variacao = "green" if variacao > 0 else "red"

    # Exibir o preço acima do gráfico
    st.markdown(f"<h2 style='color:{cor_variacao};'> {preco_atual:.2f} BRL ({variacao:.2f} BRL, {porcentagem:.2f}%)</h2>", unsafe_allow_html=True)

    # 📌 Estilizar o Gráfico de Preços com Proporção Correta
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig_price = go.Figure()

    # Definir limites do eixo Y para evitar que a linha encoste no zero
    min_preco = dados["Close"].min()
    max_preco = dados["Close"].max()
    margem = (max_preco - min_preco) * 0.1  # 10% de margem superior e inferior

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        line=dict(color='#3454b4', width=2),  # Azul atualizado
    ))

    fig_price.update_layout(
        template="plotly_white",
        title=f"Evolução do Preço - Últimos 6 Meses ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
        paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico
        font=dict(color="#ad986e"),  # Texto em dourado elegante
        xaxis=dict(showgrid=False),  # Remove grade vertical
        yaxis=dict(
            showgrid=True, 
            gridcolor="rgba(173, 152, 110, 0.2)",  # Grade dourada suave
            range=[min_preco - margem, max_preco + margem]  # Ajuste da proporção do eixo Y
        )
    )

    st.plotly_chart(fig_price)

    # 📌 GRÁFICO DE DIVIDENDOS - ÚLTIMOS 5 ANOS
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum()

        # 📌 Selecionar os últimos 5 anos disponíveis corretamente
        anos_disponiveis = dividendos.index.year
        anos_finais = anos_disponiveis[-5:]  # Pegando os últimos 5 anos reais
        dividendos = dividendos[dividendos.index.year.isin(anos_finais)]

        # 📌 Calcular o percentual de dividendos em relação ao preço médio do ano
        preco_medio_anual = dados["Close"].resample("Y").mean()
        preco_medio_anual.index = preco_medio_anual.index.year
        preco_medio_anual = preco_medio_anual.reindex(dividendos.index.year, fill_value=1)
        dividend_yield = (dividendos / preco_medio_anual) * 100  # Em %

        # ✅ Remover valores NaN e infinitos
        dividend_yield = dividend_yield.replace([float("inf"), -float("inf")], 0).fillna(0)

        # Criar gráfico estilizado com os últimos 5 anos e % no topo
        fig_divid = go.Figure()

        fig_divid.add_trace(go.Bar(
            x=dividend_yield.index.year,
            y=dividend_yield,
            text=dividend_yield.apply(lambda x: f"{x:.2f}%"),  # Exibir % diretamente nas barras
            textposition='outside',
            marker=dict(
                color="#ad986e",  # Barras douradas elegantes
                opacity=0.8,  # Suavização na cor
                line=dict(color="rgba(0, 0, 0, 0.3)", width=1),  # Contorno sutil
            )
        ))

        fig_divid.update_layout(
            template="plotly_white",
            title=f"Dividend Yield - Últimos 5 Anos ({ticker})",
            xaxis_title="Ano",
            yaxis_title="Yield (%)",
            margin=dict(l=40, r=40, t=40, b=40),
            plot_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
            paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico
            font=dict(color="#ad986e"),  # Texto em dourado elegante
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=True, gridcolor="rgba(173, 152, 110, 0.2)"),  # Grade dourada suave
        )

        st.plotly_chart(fig_divid)

        # 📌 Estatísticas de Dividendos
        st.subheader(f"📊 Estatísticas de Dividendos - {ticker}")
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_5_anos = dividendos.mean()  # Agora pega só os 5 anos
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f} ({dividend_yield.iloc[-1]:.2f}%)")
        st.write(f"🔹 **Média dos últimos 5 anos:** {media_5_anos:.2f}")
        
        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write(f"✅ **{ticker} pagou dividendos em todos os últimos 5 anos.**")
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
