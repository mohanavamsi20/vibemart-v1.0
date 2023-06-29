from flask import render_template,request, redirect, url_for, flash, session, send_from_directory
from app import app
from app.models import *
from app.forms import LoginForm, RegisterForm, AccountForm, AddressForm, SelleritemsForm
from app import db
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from xhtml2pdf import pisa
from io import BytesIO
import os
from werkzeug.utils import secure_filename
import uuid
UPLOAD_FOLDER = 'D:\\Devthon\\vibemart-v1.0\\Vibemart\\app\\static\\assets\\images\\vibemart'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def home():
    selleritems = Seller_items.query.all()
    return render_template('home.html',session=session, selleritems=selleritems)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('home'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        session['user_id'] = login_form.email.data
        account = Account.query.filter_by(email=session['user_id']).first()
        session['cart'] = Cart.query.filter_by(buyyer_id=account.id).count()
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
    seller_items = SelleritemsForm()
    user_id = session['user_id']
    accounts = Account.query.filter_by(email=user_id).all()
    selleritems = Seller_items.query.filter_by(seller_id=accounts[0].id).all()
    cart_orders = Cart.query.filter_by(buyyer_id=accounts[0].id).filter(Cart.item_status=='Ordered').all()
    if address_form.validate_on_submit():
        address_details(user_id, address_form)
        flash('Address details updated successfully!', 'address_success')
        return redirect(url_for('account'))
    if account_form.validate_on_submit():
        update_account(user_id, account_form)
        return redirect(url_for('account'))
    if seller_items.validate_on_submit():
        seller_items_funtion(user_id, seller_items)
        return redirect(url_for('account'))
    return render_template('account.html',forms = account_form ,session=session, user_id=user_id, accounts=accounts, address_form=address_form, seller_items = seller_items, selleritems = selleritems, cart_orders=cart_orders)


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


def seller_items_funtion(user_id,seller_items):
    account = Account.query.filter_by(email=user_id).first()
    if 'item_image' in request.files:
        item_picture = request.files['item_image']
        print(item_picture)
        if item_picture.filename != '':
            image_id = str(uuid.uuid4())
            image_folder = os.path.join(UPLOAD_FOLDER, image_id)
            os.makedirs(image_folder, exist_ok=True)
            filename = secure_filename(item_picture.filename)
            file_path = os.path.join(image_folder, filename)
            item_picture.save(file_path)
            print(file_path)
        else:
            item_image_path = ''
    else:
        item_image_path = ''
    if request.form['submit'] == 'SALE THE ITEM':
        if seller_items.item_offer_percentage.data == '' and seller_items.item_offer_price.data == '' and seller_items.item_offer_start_date.data == '' and seller_items.item_offer_end_date.data == '':
            item = Seller_items(
                seller_id=account.id,
                item_name=seller_items.item_name.data,
                item_description=seller_items.item_description.data,
                item_price=seller_items.item_price.data,
                item_quantity=seller_items.item_quantity.data,
                item_category=seller_items.item_category.data,
                item_image=file_path,
                item_current_status=seller_items.item_current_status.data,
                item_offer_status = seller_items.item_offer_status.data,
                item_offer_percentage = 0,
                item_offer_price = 0,
                item_offer_start_date = datetime.datetime.now(),
                item_offer_end_date = datetime.datetime.now()
            )
        else:
            item = Seller_items(
            seller_id=account.id,
            item_name=seller_items.item_name.data,
            item_description=seller_items.item_description.data,
            item_price=seller_items.item_price.data,
            item_quantity=seller_items.item_quantity.data,
            item_category=seller_items.item_category.data,
            item_image=seller_items.item_image.data,
            item_current_status=seller_items.item_current_status.data,
            item_offer_percentage=seller_items.item_offer_percentage.data,
            item_offer_price=seller_items.item_offer_price.data,
            item_offer_start_date=seller_items.item_offer_start_date.data,
            item_offer_end_date=seller_items.item_offer_end_date.data,
            item_offer_status=seller_items.item_offer_status.data
            )
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!', 'seller_item_success')
        return redirect(url_for('account'))
    elif request.form['submit'] == 'UPDATE THE ITEM':
        if seller_items.item_offer_percentage.data == '' and seller_items.item_offer_price.data == '' and seller_items.item_offer_start_date.data == '' and seller_items.item_offer_end_date.data == '':
            item = Seller_items.query.get(item_id)
            item.item_name = seller_items.item_name.data
            item.item_description = seller_items.item_description.data
            item.item_price = seller_items.item_price.data
            item.item_quantity = seller_items.item_quantity.data
            item.item_category = seller_items.item_category.data
            item.item_image = seller_items.item_image.data
            item.item_current_status = seller_items.item_current_status.data
            item.item_offer_percentage = 0
            item.item_offer_price = 0
            item.item_offer_start_date = datetime.datetime.now()
            item.item_offer_end_date = datetime.datetime.now()
        else:
            item = Seller_items.query.get(item_id)
            item.item_name = seller_items.item_name.data
            item.item_description = seller_items.item_description.data
            item.item_price = seller_items.item_price.data
            item.item_quantity = seller_items.item_quantity.data
            item.item_category = seller_items.item_category.data
            item.item_image = seller_items.item_image.data
            item.item_current_status = seller_items.item_current_status.data
            item.item_offer_percentage = seller_items.item_offer_percentage.data
            item.item_offer_price = seller_items.item_offer_price.data
            item.item_offer_start_date = seller_items.item_offer_start_date.data
            item.item_offer_end_date = seller_items.item_offer_end_date.data
            item.item_offer_status = seller_items.item_offer_status.data
        db.session.commit()
        flash('Item updated successfully!', 'seller_item_success')
        return redirect(url_for('account'))
    elif request.form['submit'] == 'DELETE THE ITEM':
        item = Seller_items.query.get(item_id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'seller_item_success')
        return redirect(url_for('account'))

# @app.route('/display/<path:filename>')
# def display_image(filename):
#     directory = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#     print(directory)
#     return send_from_directory(directory, filename)

@app.route('/display/<path:image_path>')
def display_image(image_path):
    directory = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
    print(directory)
    return send_from_directory(directory, os.path.basename(image_path))

@app.route('/shop', methods=['GET', 'POST'])
def shop():
    selleritems = Seller_items.query.all()
    return render_template('shop.html', title='Shop', selleritems=selleritems, session=session)

@app.route('/shop/<int:item_id>/add-to-cart', methods=['GET', 'POST'])
def add_to_cart(item_id):
    selleritems = Seller_items.query.get(item_id)
    user_id = session['user_id']
    account = Account.query.filter_by(email=user_id).first()
    cart_item = Cart(item_id=selleritems.item_id, item_name= selleritems.item_name,item_price=selleritems.item_price, item_quantity=1, item_status='Pending', buyyer_id=account.id, seller_id=selleritems.seller_id)
    if cart_item.seller_id == account.id:
        flash('You cannot add your own item to cart!', 'cart_error')
        return redirect(url_for('cart'))
    db.session.add(cart_item)
    db.session.commit()
    session['cart'] = Cart.query.filter_by(buyyer_id=account.id).filter(Cart.item_status=='Pending').count()
    return redirect(url_for('shop'))

@app.route('/shop/<int:item_id>/remove-from-cart', methods=['GET', 'POST'])
def remove_from_cart(item_id):
    selleritems = Seller_items.query.get(item_id)
    user_id = session['user_id']
    account = Account.query.filter_by(email=user_id).first()
    cart_item = Cart.query.filter_by(item_id=selleritems.item_id, buyyer_id=account.id).filter(Cart.item_status=='Pending').first()
    db.session.delete(cart_item)
    db.session.commit()
    session['cart'] = Cart.query.filter_by(buyyer_id=account.id).filter(Cart.item_status=='Pending').count()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    account = Account.query.filter_by(email=user_id).first()
    cart_items = Cart.query.filter_by(buyyer_id=account.id).filter(Cart.item_status=='Pending').all()
    total = 0
    for cart_item in cart_items:
        total += cart_item.item_price
    return render_template('cart.html', cart_items=cart_items,session=session, total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    account = Account.query.filter_by(email=user_id).first()
    cart_items = Cart.query.filter_by(buyyer_id=account.id).filter(Cart.item_status=='Pending').all()
    total = 0
    for cart_item in cart_items:
            total += cart_item.item_price
    if cart_items == []:
        flash('Your cart is empty!', 'cart_error')
        return redirect(url_for('cart'))
    return render_template('checkout.html', cart_items=cart_items, total=total, session=session, account=account)

@app.route('/product/<int:item_id>')
def product(item_id):
    selleritems = Seller_items.query.get(item_id)
    return render_template('product.html', title='Product', selleritems=selleritems, session=session)

@app.route('/place_order')
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    account = Account.query.filter_by(email=user_id).first()
    cart_items = Cart.query.filter_by(buyyer_id=account.id).filter(Cart.item_status=='Pending').all()
    name = account.displayname
    email = account.email
    total = 0
    for cart_item in cart_items:
        total += cart_item.item_price
    rendered_html = render_template('placeorder.html', name=name, email = email, cart_items=cart_items, account=account, session=session, total=total)

    pdf = generate_pdf(rendered_html)
    send_email(email, rendered_html, pdf)

    for cart_item in cart_items:
        cart_item.item_status = 'Ordered'
    db.session.commit()
    session.pop('cart', None)
    flash('Your order has been placed successfully!', 'order_success')
    return redirect(url_for('home'))

def generate_pdf(html):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode('utf-8')),  dest=pdf)
    return pdf.getvalue()

def send_email(to_email, html, pdf):
    # Email configuration
    sender_email = 'abc@gmail.com'
    sender_password = 'password'
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = 'Checkout PDF'

    # Attach HTML as text
    msg.attach(MIMEText(html, 'html'))

    # Attach PDF as attachment
    attachment = MIMEBase('application', 'pdf')
    attachment.set_payload(pdf)
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename='receipt.pdf')
    msg.attach(attachment)

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))