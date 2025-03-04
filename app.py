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
    st.subheader("🏢 Setor da Empresa")
    st.write(f"📌 **{setor}**")

    # Criar gráfico da cotação ao longo dos anos
    st.subheader("📈 Histórico de Preços")
    fig = px.line(dados, x=dados.index, y="Close", title=f"Evolução do Preço - {ticker}")
    st.plotly_chart(fig)

    # Buscar e exibir dividendos
    st.subheader("💰 Dividendos Anuais")
    if not stock.dividends.empty:
        stock.dividends.index = pd.to_datetime(stock.dividends.index)
        dividendos = stock.dividends.resample("Y").sum()

        # ✅ Verifica se há pelo menos um ano de dividendos antes de criar a série de anos completos
        if not dividendos.empty:
            # Criar um índice completo de anos desde o primeiro registro até o ano atual
            ano_inicio = dividendos.index.min().year
            ano_atual = pd.Timestamp.today().year
            anos_completos = pd.Series(0, index=range(ano_inicio, ano_atual + 1))

            # ✅ Mesclar os dados reais de dividendos com os anos completos
            dividendos.index = dividendos.index.year  # Converte para anos inteiros
            dividendos = anos_completos.add(dividendos, fill_value=0)

        # Criar gráfico de dividendos com valores visíveis
        fig_divid = px.bar(x=dividendos.index, 
                           y=dividendos.values, 
                           text_auto=".2f",  # Exibir valores diretamente nas barras
                           title="Valor Pago em Dividendos Anualmente")

        st.plotly_chart(fig_divid)

        # 📌 Calcular estatísticas adicionais
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_5_anos = dividendos[-5:].mean() if len(dividendos) >= 5 else dividendos.mean()
        media_historica = dividendos.mean()
        anos_sem_dividendo = dividendos[dividendos == 0].index.tolist()

        # Exibir os dados abaixo do gráfico
        st.subheader("📊 Estatísticas de Dividendos")
        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f}")
        st.write(f"🔹 **Média dos últimos 5 anos:** {media_5_anos:.2f}")
        st.write(f"🔹 **Média de dividendos (todo o histórico):** {media_historica:.2f}")
        
        if anos_sem_dividendo:
            anos_formatados = ', '.join(map(str, anos_sem_dividendo))
            st.write(f"❌ **Anos sem pagamento de dividendos:** {anos_formatados}")
        else:
            st.write("✅ **A empresa pagou dividendos em todos os anos disponíveis.**")
    else:
        st.warning("⚠️ Nenhuma informação de dividendos encontrada para esta ação.")
