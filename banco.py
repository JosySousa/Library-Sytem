# banco.py - Gerencia o banco de dados
import sqlite3

def criar_banco():
    conn = sqlite3.connect('biblioteca.db')
    c = conn.cursor()

    # Tabela de leitores
    c.execute('''
        CREATE TABLE IF NOT EXISTS leitores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT,
            telefone TEXT,
            email TEXT,
            quantidade_emprestimos INTEGER DEFAULT 0
        )
    ''')

    # Tabela de livros
    c.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT,
            quantidade INTEGER DEFAULT 0
        )
    ''')

    # Tabela de empréstimos
    c.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_leitor INTEGER,
            id_livro INTEGER,
            data_emprestimo TEXT,
            data_devolucao TEXT,
            FOREIGN KEY (id_leitor) REFERENCES leitores(id),
            FOREIGN KEY (id_livro) REFERENCES livros(id)
        )
    ''')

    conn.commit()
    conn.close()

