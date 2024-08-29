import csv
import sqlite3

# Caminho do arquivo CSV
caminho_csv = "./convidados_2.csv"

# Caminho do arquivo SQLite
caminho_sqlite = "./convidados.db"

# Conectar ao banco de dados SQLite (ele será criado se não existir)
conexao = sqlite3.connect(caminho_sqlite)
cursor = conexao.cursor()

# Criar a tabela no banco de dados SQLite
cursor.execute('''CREATE TABLE IF NOT EXISTS convidados (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    tipo TEXT,
                    confirmado BOOLEAN
                  )''')

# Ler os dados do CSV e inserir na tabela do banco de dados
with open(caminho_csv, newline='', encoding='utf-8') as arquivo_csv:
    leitor_csv = csv.DictReader(arquivo_csv, delimiter=';')
    for linha in leitor_csv:
        id_convidado = int(linha["Ord"])
        nome_convidado = linha["Nome"]
        tipo_convidado = linha["tipo"]
        confirmado = False  # Por padrão, nenhum convidado está confirmado
        cursor.execute('''INSERT INTO convidados (id, nome, tipo, confirmado) VALUES (?, ?, ?, ?)''',
                       (id_convidado, nome_convidado, tipo_convidado, confirmado))

# Salvar as alterações e fechar a conexão
conexao.commit()
conexao.close()

print("Dados do CSV importados para o banco de dados SQLite com sucesso!")
