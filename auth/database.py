import sqlite3

# Criar o banco de dados se não existir
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Criar a tabela de usuários (caso ainda não exista)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

def add_user(username, password):
    """Adiciona um novo usuário ao banco de dados."""
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def check_user(username, password):
    """Verifica se o usuário existe e a senha está correta."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None
