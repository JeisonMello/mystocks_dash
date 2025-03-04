import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Título do dashboard
st.title("📈 Dashboard de Ações")

# Entrada do usuário
ticker_input = st.text_input("Digite o código da ação (ex: AAPL, TSLA, PETR4.SA):")

# Botões de período para histórico de preços (sem afetar dividendos)
periodos = {"1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo", "YTD": "ytd", "1Y": "1y", "5Y": "5y", "Max": "max"}

# Criando os botões horizontais estilizados (padrão: 6M)
col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
botoes = [col1, col2, col3, col4, col5, col6, col7, col8]
periodo_selecionado = "6M"  # Sempre começa com 6 meses por padrão

for i, (label, value) in enumerate(periodos.items()):
    if botoes[i].button(label, key=f"btn_{label}"):
        periodo_selecionado = label  # Atualiza o período quando um botão é clicado

if ticker_input:
    ticker = ticker_input
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    # Buscar dados da ação para cotação (apenas para histórico de preços)
    stock = yf.Ticker(ticker)
    dados = stock.history(period=periodos[periodo_selecionado])

    # 📌 Independente do período, buscar os dividendos dos últimos 10 anos
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum().tail(10)  # Sempre os últimos 10 anos

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
