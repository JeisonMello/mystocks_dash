import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go

# ========================== 
# PARTE 2: HISTÓRICO DE DIVIDENDOS (WEB SCRAPING) 
# ========================== 
st.subheader("💰 Histórico de Dividendos")

# Entrada do usuário
ticker = st.text_input("Digite o código da ação (ex: BBAS3, ITSA4, CSMG3):").upper()

if ticker:
    try:
        url = f"https://statusinvest.com.br/acoes/{ticker}"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)

        # Verifica se a página foi carregada corretamente
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            # Busca os dividendos pagos por ano
            tabela_dividendos = soup.find_all("div", class_="carousel__item")
            
            dados_dividendos = []
            for item in tabela_dividendos:
                ano = item.find("h3").text.strip()  # Ano do dividendo
                valor = item.find("strong").text.strip().replace(",", ".")  # Valor do dividendo
                
                if ano.isnumeric():
                    dados_dividendos.append({"Ano": int(ano), "Dividendo": float(valor)})

            # Converte para DataFrame
            df_dividendos = pd.DataFrame(dados_dividendos)

            if not df_dividendos.empty:
                df_dividendos = df_dividendos.sort_values(by="Ano", ascending=True)

                # Criar gráfico de dividendos
                fig_dividendos = go.Figure()
                fig_dividendos.add_trace(go.Bar(
                    x=df_dividendos["Ano"],
                    y=df_dividendos["Dividendo"],
                    text=[f"{x:.2f}" for x in df_dividendos["Dividendo"]],
                    textposition='auto',
                    marker_color="#34A853"
                ))

                fig_dividendos.update_layout(
                    title="Dividendos Pagos por Ano",
                    xaxis_title="Ano",
                    yaxis_title="Dividendos (R$)",
                    template="plotly_dark"
                )

                st.plotly_chart(fig_dividendos)

                # Exibir tabela de dividendos
                st.write("📊 **Histórico de Dividendos por Ano**")
                st.dataframe(df_dividendos.rename(columns={"Ano": "Ano", "Dividendo": "Dividendos (R$)"}))

            else:
                st.warning("❌ Nenhum dividendo encontrado para esta ação no Status Invest.")

        else:
            st.error("Erro ao acessar os dados do Status Invest. Tente novamente mais tarde.")

    except Exception as e:
        st.error(f"Erro ao processar os dividendos: {e}")
