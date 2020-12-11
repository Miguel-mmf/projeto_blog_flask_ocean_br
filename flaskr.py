import sqlite3
from flask import Flask, render_template, request, g, redirect, url_for, abort, session, flash

# configuration
DATABASE = './tmp/flaskr.db'
USERNAME = 'miguel'
PASSWORD = 'nome'
SECRET_KEY = 'teste'

# criando o app
app = Flask(__name__)
app.config.from_object(__name__)

# conectar com o banco de dados
def conect_bd():
    return sqlite3.connect(DATABASE)

# abrindo o banco de dados para ser utilizado
@app.before_request
def pre_request():
    g.bd = conect_bd()

# fechando o bd quando não for utilizado, ou seja, após a requisição
@app.teardown_appcontext
def pos_request(exception):
    g.bd.close()

# primeira rota
    # selecionando todas as entradas do blog no bd por podem de id decrescente
@app.route('/')
def show_inputs():
    sql = 'SELECT title, texto FROM entradas ORDER BY id DESC'
    cursor = g.bd.execute(sql)

    entradas = [
        dict(
            titulo=title,
            texto= texto
        )
        for title, texto in cursor.fetchall()
    ]

    return render_template('show_inputs.html', entradas=entradas)

@app.route('/inserir', methods=['POST'])
def insert_content():
    if not session.get('logado'):
        abort(401)
    
    sql = 'INSERT INTO entradas (title, texto) VALUES (?, ?)'
    g.bd.execute(
        sql,
        [request.form['titulo'],request.form['texto']]
    )
    g.bd.commit()
    flash('Content inserted successfully!')

    return redirect(url_for('show_inputs'))


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'Invalid user!'
        if request.form['password'] != PASSWORD:
            error = "Invalid password"
        else:
            session['logado'] = True
            flash('Wellcome!')
        
            return redirect(url_for('show_inputs'))
    
    return render_template('login.html',erro=error)


@app.route('/logout')
def logout():
    session.pop('logado',None)
    flash('User logged out successfully!')
    
    return redirect(url_for('show_inputs'))