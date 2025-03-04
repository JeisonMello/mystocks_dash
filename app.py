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

        # Criar gráfico de dividendos com valores visíveis
        fig_divid = px.bar(x=dividendos.index.year, 
                           y=dividendos.values, 
                           text_auto=".2f",  # Exibir valores diretamente nas barras
                           title="Valor Pago em Dividendos Anualmente")

        st.plotly_chart(fig_divid)

        # 📌 Calcular estatísticas adicionais
        ultimo_dividendo = dividendos.iloc[-1] if not dividendos.empty else 0
        media_5_anos = dividendos[-5:].mean() if len(dividendos) >= 5 else dividendos.mean()
        media_historica = dividendos.mean()
        anos_sem_dividendo = dividendos[dividendos == 0].index.year.tolist()

        # Exibir os dados abaixo do gráfico
        st.subheader("📊 Estatísticas de Dividendos")
        st.write(f"🔹 **Último dividendo pago:** {ultimo_dividendo:.2f}")
        st.write(f"🔹 **Média dos últimos 5 anos:** {media_5_anos:.2f}")
        st.write(f"🔹 **Média de dividendos (todo o histórico):** {media_historica:.2f}")
        
        if anos_sem_dividendo:
            st.write(f"❌ **Anos sem pagamento de dividendos:** {', '.join(map(str, anos_sem_dividendo))}")
        else:
            st.write("✅ **A empresa pagou dividendos em todos os anos disponíveis.**")
    else:
        st.warning("⚠️ Nenhuma informação de dividendos encontrada para esta ação.")

    # 📌 Adicionar tabela com histórico de dividendos desde 2006
    st.subheader("📅 Histórico de Dividendos desde 2006")
    
    # Dados de exemplo (substitua pelos dados reais)
    dados_dividendos = {
        "Ano": [2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006],
        "Valor Pago por Ação (R$)": [0.2711, 0.5143, 0.3969, 0.3064, 0.4280, 0.7059, 0.6313, 0.2818, 0.3143, 0.4099, 0.1729, 0.2957, 0.1358, 0.3735, 0.2403, 0.1682, 0.0614, 0.1272, 0.0264]
    }
    df_dividendos = pd.DataFrame(dados_dividendos)
    st.write(df_dividendos)
