from flask import render_template,request, redirect, url_for, flash, session
from app import app
from app.forms import LoginForm, RegisterForm

@app.route('/')
def home():
    return render_template('home.html',session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['user_id'] = login_form.email.data
        return redirect(url_for('home'))
    return render_template('login.html', forms=login_form, session=session)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('home'))
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', forms=register_form, session=session)

@app.route('/success')
def success():
    return render_template('Index.html')

@app.route('/account')
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # account_form = AccountForm()
    user_id = session.get('user_id')
    return render_template('account.html',session=session, user_id=user_id)


@app.route('/update', methods=['GET', 'POST'])
def update():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    account_form = AccountForm()
    if account_form.validate_on_submit():
        flash('Update successful!', 'success')
        return redirect(url_for('account'))
    return render_template('account.html', forms=account_form, session=session)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))