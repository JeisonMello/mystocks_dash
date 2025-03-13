import sqlite3

def create_stocks_table():
    """Cria a tabela de ações no banco de dados se não existir."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            papel TEXT UNIQUE NOT NULL,
            nome TEXT,
            preco REAL,
            custava REAL,
            yield REAL,
            preco_teto REAL,
            setor TEXT,
            estrategia TEXT,
            obs TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Criar a tabela ao importar o módulo
create_stocks_table()

def add_stock(papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs):
    """Adiciona ou atualiza uma ação no banco de dados."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()

    # Verifica se a ação já existe no banco de dados
    cursor.execute("SELECT papel FROM stocks WHERE papel = ?", (papel,))
    existing_stock = cursor.fetchone()

    if existing_stock:
        # Se a ação já existe, faz uma atualização dos valores
        cursor.execute('''
            UPDATE stocks 
            SET nome = ?, preco = ?, custava = ?, yield = ?, preco_teto = ?, setor = ?, estrategia = ?, obs = ?
            WHERE papel = ?
        ''', (nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs, papel))
    else:
        # Se não existir, insere uma nova ação
        cursor.execute('''
            INSERT INTO stocks (papel, nome, preco, custava, yield, preco_teto, setor, estrategia, obs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs))

    conn.commit()
    conn.close()

def get_stocks():
    """Retorna todas as ações cadastradas."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    stocks = cursor.fetchall()
    conn.close()
    return stocks

def delete_stock(papel):
    """Remove uma ação do banco de dados pelo código do papel."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stocks WHERE papel = ?", (papel,))
    conn.commit()
    conn.close()
