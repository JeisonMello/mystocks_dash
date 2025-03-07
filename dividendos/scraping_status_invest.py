import requests
from bs4 import BeautifulSoup
import pandas as pd

def coletar_dividendos(ticker):
    url = f"https://statusinvest.com.br/acoes/{ticker}"
    
    # Fazendo a requisição para o site
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Erro ao acessar o Status Invest.")
        return None

    # Parseando o HTML
    soup = BeautifulSoup(response.text, "html.parser")

    # Encontrando a tabela de dividendos
    tabela = soup.find("table", {"id": "earning-results"})  # ID pode mudar, verificar no site
    if not tabela:
        print("Tabela de dividendos não encontrada.")
        return None

    # Extraindo os dados
    dados = []
    linhas = tabela.find_all("tr")[1:]  # Ignorar cabeçalho

    for linha in linhas:
        colunas = linha.find_all("td")
        ano = colunas[0].text.strip()
        valor = colunas[1].text.strip()
        dados.append([ano, valor])

    # Criando DataFrame
    df = pd.DataFrame(dados, columns=["Ano", "Dividendos"])

    return df

# Testando a função
if __name__ == "__main__":
    ticker = "PETR4"
    df_dividendos = coletar_dividendos(ticker)

    if df_dividendos is not None:
        print(df_dividendos)
    else:
        print("Falha ao coletar os dividendos.")
