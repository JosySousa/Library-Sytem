import sqlite3
from datetime import datetime

def conectar():
    return sqlite3.connect('biblioteca.db')

def cadastrar_leitor(nome, endereco, telefone, email):
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
        INSERT INTO leitores (nome, endereco, telefone, email)
        VALUES (?, ?, ?, ?)
    ''', (nome, endereco, telefone, email))
    conn.commit()
    conn.close()

def cadastrar_livro(titulo, autor, quantidade):
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
        INSERT INTO livros (titulo, autor, quantidade)
        VALUES (?, ?, ?)
    ''', (titulo, autor, quantidade))
    conn.commit()
    conn.close()

def emprestar_livro(id_leitor, id_livro):
    conn = conectar()
    c = conn.cursor()

    # Verificar disponibilidade do livro
    c.execute('SELECT quantidade FROM livros WHERE id = ?', (id_livro,))
    quantidade = c.fetchone()[0]

    if quantidade > 0:
        data_emprestimo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute(''' 
            INSERT INTO emprestimos (id_leitor, id_livro, data_emprestimo)
            VALUES (?, ?, ?)
        ''', (id_leitor, id_livro, data_emprestimo))

        # Atualizar quantidade de livros
        c.execute('UPDATE livros SET quantidade = quantidade - 1 WHERE id = ?', (id_livro,))

        # Atualizar a quantidade de empréstimos do leitor
        c.execute('UPDATE leitores SET quantidade_emprestimos = quantidade_emprestimos + 1 WHERE id = ?', (id_leitor,))

        conn.commit()
        print(f"Empréstimo realizado com sucesso para o leitor com ID {id_leitor} e o livro com ID {id_livro}.")
    else:
        print("Livro não disponível para empréstimo.")

    conn.close()


def devolver_livro(id_leitor, id_livro):
    conn = conectar()
    c = conn.cursor()

    data_devolucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute(''' 
        UPDATE emprestimos SET data_devolucao = ? 
        WHERE id_leitor = ? AND id_livro = ? AND data_devolucao IS NULL
    ''', (data_devolucao, id_leitor, id_livro))

    # Atualizar quantidade de livros
    c.execute('UPDATE livros SET quantidade = quantidade + 1 WHERE id = ?', (id_livro,))

    # Atualizar quantidade de empréstimos do leitor
    c.execute('UPDATE leitores SET quantidade_emprestimos = quantidade_emprestimos - 1 WHERE id = ?', (id_leitor,))

    conn.commit()
    conn.close()

def listar_emprestimos(id_leitor):
    conn = conectar()
    c = conn.cursor()
    c.execute(''' 
        SELECT livros.titulo, emprestimos.data_emprestimo, emprestimos.data_devolucao
        FROM emprestimos
        JOIN livros ON emprestimos.id_livro = livros.id
        WHERE emprestimos.id_leitor = ?
    ''', (id_leitor,))
    emprestimos = c.fetchall()
    conn.close()
    return emprestimos

# NOVAS FUNÇÕES ADICIONADAS

def buscar_leitores_por_nome(nome):
    conn = conectar()
    c = conn.cursor()
    c.execute("SELECT * FROM leitores WHERE nome LIKE ?", ('%' + nome + '%',))
    leitores = c.fetchall()
    conn.close()
    return leitores


def buscar_livros_por_nome(nome):
    conn = conectar()
    c = conn.cursor()
    c.execute('''SELECT * FROM livros WHERE titulo LIKE ?''', ('%' + nome + '%',))  # % é para permitir a busca parcial
    livros = c.fetchall()
    conn.close()
    return livros
