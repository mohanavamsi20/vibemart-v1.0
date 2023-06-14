from flask import render_template,request, redirect, url_for, flash, session
from app import app
from app.models import User, Account
from app.forms import LoginForm, RegisterForm, AccountForm, AddressForm
from app import db

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

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    account_form = AccountForm()
    address_form = AddressForm()
    user_id = session['user_id']
    accounts = Account.query.filter_by(email=user_id).all()
    if address_form.validate_on_submit():
        address_details(user_id, address_form)
        flash('Address details updated successfully!', 'address_success')
        return redirect(url_for('account'))
    if account_form.validate_on_submit():
        update_account(user_id, account_form)
        return redirect(url_for('account'))
    return render_template('account.html',forms = account_form ,session=session, user_id=user_id, accounts=accounts, address_form=address_form)


def update_account(user_id,account_form):
    account = Account.query.filter_by(email=user_id).first()
    user = User.query.filter_by(email=user_id).first()
    if account_form.new_password.data:
        if account_form.current_password.data:
            if account_form.current_password.data == user.password:
                if account_form.new_password.data == account_form.confirm_password.data:
                    if account_details(account_form, account):
                        db.session.commit()
                    user.password = account_form.new_password.data
                    account.password = account_form.new_password.data
                    flash('Account details updated successfully with Password', 'success')
                    db.session.commit()
                else:
                    flash('New password and confirm password do not match!', 'danger')
            else:
                flash('Current password is incorrect!', 'danger')
        else:
            flash('Current password cannot be empty!', 'danger')
    else:
        if account_details(account_form, account):
            flash('Account details updated successfully!', 'success')
            db.session.commit()


def account_details(account_form, account):
    flag = False
    if account_form.firstname.data or account_form.lastname.data or account_form.displayname.data:
        if account_form.firstname.data != account.firstname:
            account.firstname = account_form.firstname.data
            flag = True
        if account_form.lastname.data != account.lastname:
            account.lastname = account_form.lastname.data
            flag = True
        if account_form.displayname.data != account.displayname:
            account.displayname = account_form.displayname.data
            flag = True
    return flag

def address_details(user_id,address_form):
    account = Account.query.filter_by(email=user_id).first()
    account.address_line1 = address_form.address_line1.data
    account.address_line2 = address_form.address_line2.data
    account.country = address_form.country.data
    account.city = address_form.city.data
    account.state = address_form.state.data
    account.zipcode = address_form.zip_code.data
    account.phone = address_form.phone.data
    db.session.commit()


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))