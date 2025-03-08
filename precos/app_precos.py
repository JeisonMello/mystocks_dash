import yfinance as yf
import plotly.graph_objects as go

def carregar_grafico_precos(ticker):
    """ Carrega e retorna o gráfico de histórico de preços de uma ação """

    # Formatar o ticker
    ticker = ticker.upper()
    if not ticker.endswith(".SA") and len(ticker) == 5:
        ticker += ".SA"

    try:
        # Buscar dados da ação
        stock = yf.Ticker(ticker)
        stock_info = stock.info  

        # Verificar se os dados são válidos
        if not stock_info or "longName" not in stock_info:
            raise ValueError("Ação não localizada")

        moeda = stock_info.get("currency", "N/A")  # Obtém a moeda da ação

        # Pega os dados históricos da ação
        dados = stock.history(period="6mo")

        # Determina a cor do gráfico
        cor_grafico = "#34A853" if stock_info.get("regularMarketChange", 0) > 0 else "#EA4335"
        transparencia = "rgba(52, 168, 83, 0.2)" if stock_info.get("regularMarketChange", 0) > 0 else "rgba(234, 67, 53, 0.2)"

        # Criação do gráfico
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dados.index, 
            y=dados["Close"], 
            mode='lines',
            fill='tozeroy',
            line=dict(color=cor_grafico, width=2),
            fillcolor=transparencia,
            hovertemplate=f'<b>%{{y:.2f}} {moeda}</b><br>%{{x|%d %b %y}}<extra></extra>'
        ))

        fig.update_layout(
            template="plotly_white",
            title=f"Histórico de Preços - {ticker}",
            xaxis_title="Data",
            yaxis_title=f"Preço ({moeda})",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        return fig

    except Exception as e:
        print(f"Erro ao carregar os dados de {ticker}: {e}")
        return None
