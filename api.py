from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

# Conectar ao banco de dados
def conectar():
    return sqlite3.connect('biblioteca.db')

# Rota para cadastrar leitores
@app.route('/leitores', methods=['POST'])
def cadastrar_leitor():
    dados = request.json
    conn = conectar()
    c = conn.cursor()
    c.execute('''INSERT INTO leitores (nome, endereco, telefone, email) VALUES (?, ?, ?, ?)''',
              (dados['nome'], dados['endereco'], dados['telefone'], dados['email']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Leitor cadastrado com sucesso!'}), 201

# Rota para listar leitores
@app.route('/leitores', methods=['GET'])
def listar_leitores():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM leitores')
    leitores = c.fetchall()
    conn.close()
    return jsonify(leitores)

# Rota para cadastrar livro
@app.route('/livros', methods=['POST'])
def cadastrar_livro():
    dados = request.json
    conn = conectar()
    c = conn.cursor()
    c.execute('''INSERT INTO livros (titulo, autor, quantidade) VALUES (?, ?, ?)''',
              (dados['titulo'], dados['autor'], dados['quantidade']))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Livro cadastrado com sucesso!'}), 201

# Rota para listar livros
@app.route('/livros', methods=['GET'])
def listar_livros():
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM livros')
    livros = c.fetchall()
    conn.close()
    return jsonify(livros)

# Rota para emprestar um livro
@app.route('/emprestar', methods=['POST'])
def emprestar_livro():
    dados = request.json
    id_leitor = dados['id_leitor']
    id_livro = dados['id_livro']
    conn = conectar()
    c = conn.cursor()
    
    # Verifica se o livro está disponível
    c.execute('SELECT quantidade FROM livros WHERE id = ?', (id_livro,))
    quantidade = c.fetchone()[0]

    if quantidade > 0:
        data_emprestimo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        c.execute('''INSERT INTO emprestimos (id_leitor, id_livro, data_emprestimo) VALUES (?, ?, ?)''',
                  (id_leitor, id_livro, data_emprestimo))
        c.execute('UPDATE livros SET quantidade = quantidade - 1 WHERE id = ?', (id_livro,))
        conn.commit()
        conn.close()
        return jsonify({'mensagem': 'Empréstimo realizado com sucesso!'}), 200
    else:
        conn.close()
        return jsonify({'erro': 'Livro indisponível para empréstimo'}), 400

# Rota para devolver um livro
@app.route('/devolver', methods=['POST'])
def devolver_livro():
    dados = request.json
    id_leitor = dados['id_leitor']
    id_livro = dados['id_livro']
    conn = conectar()
    c = conn.cursor()

    data_devolucao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''UPDATE emprestimos SET data_devolucao = ? WHERE id_leitor = ? AND id_livro = ? AND data_devolucao IS NULL''',
              (data_devolucao, id_leitor, id_livro))
    c.execute('UPDATE livros SET quantidade = quantidade + 1 WHERE id = ?', (id_livro,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Livro devolvido com sucesso!'}), 200

# Iniciar a API
if __name__ == '__main__':
    app.run(debug=True)
