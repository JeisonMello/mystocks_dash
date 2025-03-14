import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from auth.database_stocks import get_stocks

def plot_stock_chart(ticker, period="6mo"):
    """ Obtém e exibe o gráfico de preços da ação """
    stock = yf.Ticker(ticker + ".SA")
    df = stock.history(period=period)

    if df.empty:
        st.warning("Nenhum dado disponível para este período.")
        return

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["Close"],
        mode="lines",
        fill='tozeroy',
        line=dict(color="red"),
        name="Preço"
    ))

    fig.update_layout(
        title=f"Histórico de Preços de {ticker}",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)


def dashboard_stocks():
    st.title("📊 Dashboard - Ações Monitoradas")

    # Obter dados das ações cadastradas
    stocks = get_stocks()
    if stocks:
        df = pd.DataFrame(stocks, columns=["ID", "Papel", "Empresa", "Preço", "Custava", "Yield", "Teto", "Setor", "Estratégia", "Obs"])
        df = df.drop(columns=["ID"])  # Oculta a coluna ID
        df["Yield"] = df["Yield"].apply(lambda x: f"{x:.2f}%")  # Formatar Yield

        # Criar um índice clicável para abrir detalhes
        selected_ticker = st.session_state.get("selected_ticker", None)

        # Exibir a tabela estilizada
        st.dataframe(df.style.applymap(lambda x: "background-color: #333333; color: white" if df.index.get_loc(x) % 2 == 0 else "background-color: #222222; color: white"))

        # Adicionar funcionalidade de clique
        for index, row in df.iterrows():
            if st.button(f"🔍 {row['Papel']}", key=f"btn_{row['Papel']}"):
                st.session_state["selected_ticker"] = row['Papel']
                st.session_state["selected_empresa"] = row['Empresa']
                st.session_state["selected_preco"] = row['Preço']
                st.rerun()

        # Exibir detalhes da ação clicada
        if selected_ticker:
            show_stock_details(selected_ticker, st.session_state["selected_empresa"], st.session_state["selected_preco"])

    else:
        st.warning("Nenhuma ação cadastrada ainda.")


def show_stock_details(ticker, empresa, preco):
    """ Exibe o painel de detalhes da ação clicada """
    st.subheader(f"📈 {empresa} ({ticker})")

    # Barra de seleção de período
    periods = {
        "1D": "1d",
        "5D": "5d",
        "1M": "1mo",
        "6M": "6mo",
        "YTD": "ytd",
        "1Y": "1y",
        "5Y": "5y",
        "All": "max"
    }

    # Exibir o preço atual com variação
    stock = yf.Ticker(ticker + ".SA")
    info = stock.info
    variation = info.get("regularMarketChangePercent", 0.0)

    col1, col2 = st.columns([1, 3])
    with col1:
        st.metric(label="Preço Atual", value=f"R$ {preco:.2f}", delta=f"{variation:.2f}%")

    # Barra de período
    selected_period = st.selectbox("Selecione o período", list(periods.keys()), index=3, key="chart_period")

    # Exibir gráfico
    plot_stock_chart(ticker, periods[selected_period])
