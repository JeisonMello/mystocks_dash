import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Estilização CSS para alinhar os elementos ao estilo do Google Finance
st.markdown("""
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        h2 {
            font-size: 32px !important;
            font-weight: bold !important;
            margin-bottom: 0px !important;
        }
        .subtext {
            font-size: 20px !important;
            font-weight: normal !important;
            color: #999999 !important;
        }
        .positive {
            color: #34A853 !important;
            font-size: 20px !important;
        }
        .negative {
            color: #EA4335 !important;
            font-size: 20px !important;
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
st.title("📊 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação
    stock = yf.Ticker(ticker)
    dados = stock.history(period="10y")

    # Buscar preço atual
    preco_atual = dados["Close"].iloc[-1]
    preco_anterior = dados["Close"].iloc[0]
    variacao = preco_atual - preco_anterior
    porcentagem = (variacao / preco_anterior) * 100
    cor_variacao = "positive" if variacao > 0 else "negative"
    simbolo_variacao = "▲" if variacao > 0 else "▼"

    # Exibir o preço da ação seguindo o padrão do Google Finance
    st.markdown(f"""
        <h2>{preco_atual:.2f} BRL <span class="subtext">BRL</span></h2>
        <p class="{cor_variacao}">{simbolo_variacao} {variacao:.2f} ({porcentagem:.2f}%) hoje</p>
    """, unsafe_allow_html=True)

    # =====================================
    # 📌 PARTE 01 - HISTÓRICO DE PREÇOS
    # =====================================

    st.subheader(f"📈 Histórico de Preços - {ticker}")

    # Ajustar a escala do gráfico para não começar em zero
    min_preco = dados["Close"].min() * 0.98  # Ajusta um pouco abaixo do mínimo
    max_preco = dados["Close"].max() * 1.02  # Ajusta um pouco acima do máximo

    fig_price = go.Figure()

    fig_price.add_trace(go.Scatter(
        x=dados.index, 
        y=dados["Close"], 
        mode='lines',
        fill='tozeroy',  # Preenchimento suave
        line=dict(color='#4285F4', width=2),  # Azul Google Finance mais fino
        fillcolor='rgba(66, 133, 244, 0.2)'  # Transparência suave no fundo
    ))

    fig_price.update_layout(
        template="plotly_white",
        title=f"Evolução do Preço - {ticker}",
        xaxis_title="",  # Remove a legenda "Ano"
        yaxis_title="Preço (R$)",
        margin=dict(l=40, r=40, t=40, b=40),
        plot_bgcolor="rgba(0,0,0,0)",  # Fundo transparente
        paper_bgcolor="rgba(0,0,0,0)",  # Fundo da área do gráfico
        font=dict(color="white"),  # Texto branco
        xaxis=dict(showgrid=False),  # Remove grade vertical
        yaxis=dict(showgrid=True, gridcolor="rgba(200, 200, 200, 0.2)", range=[min_preco, max_preco])  # Ajusta a escala do eixo Y
    )

    st.plotly_chart(fig_price)

    # =====================================
    # 📌 PARTE 02 - DIVIDENDOS ANUAIS (CORRIGIDO)
    # =====================================

    st.subheader(f"💰 Dividendos Anuais - {ticker}")

    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum().tail(10)  # PEGANDO OS ÚLTIMOS 10 ANOS

        # 📌 Garantir que todos os anos tenham valores (mesmo que seja 0)
        ano_inicio = dividendos.index.min()
        ano_atual = pd.Timestamp.today().year
        anos_completos = pd.Series(0, index=range(ano_inicio, ano_atual + 1))
        dividendos.index = dividendos.index.year
        dividendos = anos_completos.add(dividendos, fill_value=0)

        # 📌 Calcular o percentual de dividendos em relação ao preço médio do ano
        preco_medio_anual = stock.history(period="10y")["Close"].resample("Y").mean()
        preco_medio_anual.index = preco_medio_anual.index.year
        preco_medio_anual = preco_medio_anual.reindex(dividendos.index, fill_value=1)
        dividend_yield = (dividendos / preco_medio_anual) * 100  

        dividend_yield = dividend_yield.replace([float("inf"), -float("inf")], 0).fillna(0)

        # Criar gráfico correto de barras, um para cada ano
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
            xaxis_title="Ano",  # Certifique-se de manter a legenda correta para os anos
            yaxis_title="Yield (%)",
            margin=dict(l=40, r=40, t=40, b=40),
            font=dict(color="white")
        )

        st.plotly_chart(fig_divid)

        # 📌 Estatísticas de Dividendos
        st.subheader(f"📊 Estatísticas de Dividendos - {ticker}")
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_10_anos = dividendos.mean()
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f} ({dividend_yield.iloc[-1]:.2f}%)")
        st.write(f"🔹 **Média dos últimos 10 anos:** {media_10_anos:.2f}")

        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write(f"✅ **{ticker} pagou dividendos em todos os últimos 10 anos.**")
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
