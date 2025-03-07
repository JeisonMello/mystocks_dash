import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("Histórico de Preços 📈")

# Entrada do usuário para o ticker da ação
ticker_input = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):")

if ticker_input:
    ticker = ticker_input.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    try:
        # Buscar dados da ação
        stock = yf.Ticker(ticker)
        stock_info = stock.info  

        # Verificar se os dados são válidos
        if not stock_info or "longName" not in stock_info:
            raise ValueError("Ação não localizada")

        company_name = stock_info.get("longName", ticker)
        moeda = stock_info.get("currency", "N/A")  # Obtém a moeda da ação

        st.markdown(f"<h2 style='color: white; font-size: 22px;'>{company_name} ({ticker})</h2>", unsafe_allow_html=True)

        # Seletor de período
        periodos = {
            "1D": "1d", "5D": "5d", "1M": "1mo", "6M": "6mo",
            "YTD": "ytd", "1Y": "1y", "5Y": "5y", "ALL": "max"
        }

        if "periodo_selecionado" not in st.session_state:
            st.session_state["periodo_selecionado"] = "6M"

        colunas = st.columns(len(periodos))
        for i, (p, v) in enumerate(periodos.items()):
            with colunas[i]:
                if st.button(p, key=p):
                    st.session_state["periodo_selecionado"] = p

        # Atualizar dados conforme período selecionado
        periodo = periodos[st.session_state["periodo_selecionado"]]
        dados = stock.history(period=periodo)

        # Gráfico de histórico de preços
        cor_grafico = "#34A853" if stock_info.get("regularMarketChange", 0) > 0 else "#EA4335"
        transparencia = "rgba(52, 168, 83, 0.2)" if stock_info.get("regularMarketChange", 0) > 0 else "rgba(234, 67, 53, 0.2)"

        fig_price = go.Figure()
        fig_price.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color=cor_grafico, width=2),
            fillcolor=transparencia,
            hovertemplate=f'<b>%{{y:.2f}} {moeda}</b><br>%{{x|%d %b %y}}<extra></extra>'
        ))

        fig_price.update_layout(
            template="plotly_white",
            title="Histórico de Preços",
            xaxis_title="Data",
            yaxis_title=f"Preço ({moeda})",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig_price)

    except Exception as e:
        st.error("Ação não localizada, insira o código de uma ação existente.")
