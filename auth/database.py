import sqlite3

# Criar o banco de dados e a tabela se não existirem
conn = sqlite3.connect("users.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

def check_email_exists(email):
    """Verifica se o e-mail já está cadastrado no banco de dados."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None  # Retorna True se o e-mail já existir

def add_user(email, password):
    """Adiciona um novo usuário ao banco de dados, verificando se o e-mail já existe."""
    if check_email_exists(email):
        return "exists"  # Retorna que o e-mail já está cadastrado

    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
        conn.commit()
        conn.close()
        return "success"  # Retorna sucesso ao cadastrar
    except Exception as e:
        return f"error: {str(e)}"  # Retorna erro específico

def delete_user(email):
    """Exclui um usuário do banco de dados pelo e-mail."""
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE email = ?", (email,))
    conn.commit()
    conn.close()
    return "Usuário excluído com sucesso!"
