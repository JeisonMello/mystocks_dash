

def debug_stock_data(papel):
    """Depuração: Exibir todos os dados da API do Yahoo Finance"""
    papel_formatado = papel + ".SA"  # Yahoo Finance usa ".SA" para ações brasileiras
    stock = yf.Ticker(papel_formatado)
    info = stock.info  # Obtem todas as informações disponíveis
    st.write(info)  # Exibe os dados para depuração no Streamlit

# Adicione abaixo do campo de entrada do papel
if papel:
    debug_stock_data(papel)  # Vai imprimir todas as informações do Yahoo Finance
