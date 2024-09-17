from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def conectar_db():
    conectar = sqlite3.connect('produtos.db')
    conectar.row_factory = sqlite3.Row 
    return conectar


def criar_tabela():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL,
            quantidade INTEGER)
    ''')
    conectar.commit()
    conectar.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add_prod_novo', methods=['POST'])
def adicionar_produto_novo():
    produto = request.form['produto']
    quantidade = request.form['quantidade']
    

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        'INSERT INTO produtos (produto, quantidade) VALUES (?,?)', (produto , quantidade)
    )
    conectar.commit()
    conectar.close()
    return redirect(url_for('index'))




@app.route('/add_prod', methods=['POST'])
def adicionar_produto():
    produto = request.form['produto']
    
    quantidade = request.form['quantidade']
    

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
        "SELECT quantidade FROM produtos WHERE produto=? " , [produto])
    resultado = cursor.fetchone()
    estoque_atual = resultado[0]
    atual = estoque_atual + int(quantidade)
    cursor.execute("UPDATE produtos SET quantidade=? WHERE produto = ? ", [atual , produto])
    conectar.commit()
    conectar.close()
    return redirect(url_for('index'))



@app.route('/remover_prod', methods=['POST'])
def remover_produto():
    produto = request.form['produto']
    quantidade = request.form['quantidade']
    quantidade = int(quantidade)

    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute(
            "SELECT quantidade FROM produtos WHERE produto=? " , [produto])
    
    resultado = cursor.fetchone()
    estoque_atual = resultado[0]
    if estoque_atual >= quantidade: 
        cursor.execute("UPDATE produtos SET quantidade=? WHERE produto = ?", [estoque_atual - quantidade , produto])
        conectar.commit()
        conectar.close()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/produtos')
def listar_estudantes():
    conectar = conectar_db()
    cursor = conectar.cursor()
    cursor.execute('SELECT * FROM produtos')
    produtos = cursor.fetchall()
    conectar.close()


    return render_template('produtos.html', produtos=produtos)



if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True, port=8080)