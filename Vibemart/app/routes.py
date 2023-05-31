from flask import render_template,request, redirect, url_for, flash
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('success'))
    return render_template('login.html', forms=login_form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', forms=register_form)

@app.route('/success')
def success():
    return render_template('Index.html')
