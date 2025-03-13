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
    """Adiciona uma nova ação ou atualiza uma já existente no banco de dados."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()

    try:
        # Verifica se a ação já existe no banco de dados
        cursor.execute("SELECT * FROM stocks WHERE papel = ?", (papel,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Atualiza os dados caso a ação já exista
            cursor.execute('''
                UPDATE stocks 
                SET nome = ?, preco = ?, custava = ?, yield = ?, preco_teto = ?, setor = ?, estrategia = ?, obs = ?
                WHERE papel = ?
            ''', (nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs, papel))
            msg = f"Ação {papel} já existia e foi atualizada com sucesso!"
        else:
            # Insere nova ação caso ainda não exista
            cursor.execute('''
                INSERT INTO stocks (papel, nome, preco, custava, yield, preco_teto, setor, estrategia, obs)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (papel, nome, preco, custava, yield_val, preco_teto, setor, estrategia, obs))
            msg = f"Ação {papel} adicionada com sucesso!"

        conn.commit()
    except sqlite3.Error as e:
        msg = f"Erro ao adicionar ou atualizar ação {papel}: {e}"
    finally:
        conn.close()
    
    return msg  # Retorna uma mensagem indicando se foi adicionado ou atualizado

def get_stocks():
    """Retorna todas as ações cadastradas."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM stocks")
    stocks = cursor.fetchall()
    conn.close()
    return stocks

def delete_stock(papel):
    """Remove uma ação do banco de dados pelo código do papel, se existir."""
    conn = sqlite3.connect("stocks.db")
    cursor = conn.cursor()

    try:
        # Verifica se a ação existe antes de remover
        cursor.execute("SELECT * FROM stocks WHERE papel = ?", (papel,))
        stock = cursor.fetchone()

        if stock:
            cursor.execute("DELETE FROM stocks WHERE papel = ?", (papel,))
            conn.commit()
            msg = f"Ação {papel} removida com sucesso!"
        else:
            msg = f"Ação {papel} não encontrada no banco de dados."

    except sqlite3.Error as e:
        msg = f"Erro ao excluir ação {papel}: {e}"

    finally:
        conn.close()
    
    return msg
