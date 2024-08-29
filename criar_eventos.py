import sqlite3

caminho_sqlite = "./convidados.db"

# Conectar ao banco de dados SQLite (ele será criado se não existir)
conexao = sqlite3.connect(caminho_sqlite)
cursor = conexao.cursor()

# Criar a tabela no banco de dados SQLite
cursor.execute('''CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    data DATE
                  )''')

# Salvar as alterações e fechar a conexão
conexao.commit()
conexao.close()

print("Tabela criada com sucesso!")
