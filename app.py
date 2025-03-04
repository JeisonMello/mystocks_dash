import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

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

    # Criar gráfico da cotação ao longo dos anos
    st.subheader(f"📈 Histórico de Preços - {ticker}")
    fig = px.line(dados, x=dados.index, y="Close", title=f"Evolução do Preço - {ticker}")
    st.plotly_chart(fig)

    # Buscar e exibir dividendos
    st.subheader(f"💰 Dividendos Anuais - {ticker}")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum()

        # 📌 Garantir que todos os anos tenham valores (mesmo que seja 0)
        ano_inicio = dividendos.index.min().year
        ano_atual = pd.Timestamp.today().year
        anos_completos = pd.Series(0, index=range(ano_inicio, ano_atual + 1))
        dividendos.index = dividendos.index.year
        dividendos = anos_completos.add(dividendos, fill_value=0)

        # 📌 Calcular o percentual de dividendos em relação ao preço médio do ano
        preco_medio_anual = dados["Close"].resample("Y").mean()
        preco_medio_anual.index = preco_medio_anual.index.year

        # ✅ Preencher anos sem preços médios para evitar erro
        preco_medio_anual = preco_medio_anual.reindex(dividendos.index, fill_value=1)

        dividend_yield = (dividendos / preco_medio_anual) * 100  # Em %

        # ✅ Remover valores NaN e infinitos
        dividend_yield = dividend_yield.replace([float("inf"), -float("inf")], 0).fillna(0)

        # Criar gráfico de dividendos com valores em %
        if not dividend_yield.empty:
            fig_divid = px.bar(
                x=dividend_yield.index,
                y=dividend_yield,
                text=dividend_yield.apply(lambda x: f"{x:.2f}%"),  # Exibir % nas barras
                title=f"Dividend Yield Anual - {ticker}"
            )
            st.plotly_chart(fig_divid)
        else:
            st.warning(f"⚠️ Não há dividendos suficientes para exibir um gráfico válido para {ticker}.")

        # 📌 Calcular estatísticas adicionais
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_5_anos = dividendos[-5:].mean() if len(dividendos) >= 5 else dividendos.mean()
        media_historica = dividendos.mean()
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        # Exibir os dados abaixo do gráfico
        st.subheader(f"📊 Estatísticas de Dividendos - {ticker}")
        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f} ({dividend_yield.iloc[-1]:.2f}%)")
        st.write(f"🔹 **Média dos últimos 5 anos:** {media_5_anos:.2f}")
        st.write(f"🔹 **Média de dividendos (todo o histórico):** {media_historica:.2f}")
        
        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write(f"✅ **{ticker} pagou dividendos em todos os anos disponíveis.**")
    else:
        st.warning(f"⚠️ Nenhuma informação de dividendos encontrada para {ticker}.")
