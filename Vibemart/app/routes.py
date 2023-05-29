from flask import render_template
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html')

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template('register.html')
