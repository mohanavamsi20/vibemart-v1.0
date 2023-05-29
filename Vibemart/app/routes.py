# app/routes.py
from flask import render_template, request, redirect, session
from app import app, mysql

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cursor.close()
        return redirect('/login')
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            session['username'] = user['username']
            return redirect('/')
        else:
            return render_template('index-1.html', error='Invalid username or password')
    return render_template('Index.html')

