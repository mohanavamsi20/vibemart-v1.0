# from flask import render_template,request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User, Account, Seller_items
from app import db 

class LoginForm(FlaskForm):
    email = StringField('signin-email', validators=[InputRequired(), Length(min=4, max=120)])
    password = PasswordField('signin-password', validators=[InputRequired(), Length(min=4, max=60)])
    submit = SubmitField('LOGIN')   

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Email does not exist')
        if user.password != self.password.data:
            raise ValidationError('Password is incorrect')
        return user

    
class RegisterForm(FlaskForm):
    email = StringField('register-email-2', validators=[InputRequired(), Length(min=4, max=120)])
    password = PasswordField('register-password-2', validators=[InputRequired(), Length(min=4, max=60)])
    role = SelectField('Role', choices=[('buyer', 'Buyer'), ('seller', 'Seller')])
    submit = SubmitField('REGISTER')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
        new_user = User(email=email.data, password=self.password.data)
        new_account = Account(email=email.data, password=self.password.data, role=self.role.data)
        db.session.add(new_user)
        db.session.add(new_account)
        db.session.commit()
        

class AccountForm(FlaskForm):
    firstname = StringField('firstname', validators=[validators.Optional(),InputRequired()])
    lastname = StringField('lastname', validators=[validators.Optional(),InputRequired()])
    displayname = StringField('displayname', validators=[validators.Optional(),InputRequired(), Length(min=4, max=120)])
    email = StringField('email', validators=[Length(min=4, max=120)], render_kw={'readonly': True})
    current_password = PasswordField('password', validators=[validators.Optional(),Length(min=4, max=60)])
    new_password = PasswordField('new_password', validators=[validators.Optional(),Length(min=4, max=60)])
    confirm_password = PasswordField('confirm_password', validators=[validators.Optional(),Length(min=4, max=60)])
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'btn btn-outline-primary-2'})

class AddressForm(FlaskForm):
    address_line1 = StringField('address_line_1', validators=[InputRequired(),Length(min=1, max=35)])
    address_line2 = StringField('address_line_2', validators=[InputRequired(), Length(min=1, max=35)])
    country = StringField('country', validators=[InputRequired()])
    state = StringField('state', validators=[InputRequired()])
    city = StringField('city', validators=[InputRequired()])
    zip_code = StringField('zip_code', validators=[InputRequired()])
    phone = StringField('phone', validators=[InputRequired()])
    submit = SubmitField('SAVE CHANGES', render_kw={'class': 'btn btn-outline-primary-2'})

class SelleritemsForm(FlaskForm):
    item_name = StringField('item_name', validators=[InputRequired(message='Please enter the item name.')])
    item_price = StringField('item_price', validators=[InputRequired(message='Please enter the item price.')])
    item_description = StringField('item_description', validators=[InputRequired(message='Please enter the item description.')])
    item_image = FileField('item_image', validators=[validators.Optional()])
    item_category = SelectField('item_category', validators=[InputRequired(message='Please Select category')], choices=[
        ('SELECT ITEM CATEGORY', 'SELECT ITEM CATEGORY'),
        ('ACCESSORIES', 'ACCESSORIES'),
        ('LIGHTING', 'LIGHTING'),
        ('MOSS POLES & PLANT SUPPORTS', 'MOSS POLES & PLANT SUPPORTS'),
        ('NUTRIENTS', 'NUTRIENTS'),
        ('PLANTS', 'PLANTS'),
        ('PLANT CARE', 'PLANT CARE'),
        ('POTS', 'POTS'),
        ('COFFEE & TABLES', 'COFFEE & TABLES'),
        ('SUBSTRATES', 'SUBSTRATES'),
    ])
    item_current_status = SelectField('item_current_status', validators=[InputRequired(message='Please select Current Status')], choices=[
        ('SELECT ITEM STATUS', 'SELECT ITEM STATUS'),
        ('AVAILABLE', 'AVAILABLE'),
        ('SOLD', 'SOLD'),
        ('OUT OF STOCK', 'OUT OF STOCK'),
    ])
    item_quantity = IntegerField('item_quantity', validators=[InputRequired(message='Please enter the item quantity.')])
    item_offer_percentage = IntegerField('item_offer_percentage', validators=[validators.Optional()])
    item_offer_price = IntegerField('item_offer_price', validators=[validators.Optional()])
    item_offer_start_date = DateField('item_offer_start_date', validators=[validators.Optional()])
    item_offer_end_date = DateField('item_offer_end_date', validators=[validators.Optional()])
    item_offer_status = SelectField('item_offer_status', validators=[validators.Optional()], choices=[
            ('SELECT OFFER STATUS', 'SELECT OFFER STATUS'),
            ('ON OFFER', 'ON OFFER'),
            ('NOT ON OFFER', 'NOT ON OFFER'),
            ('OFFER EXPIRED', 'OFFER EXPIRED'),
            ('TO BE ON OFFER', 'TO BE ON OFFER'),
    ], default='NOT ON OFFER')
    submit = SubmitField('SALE THE ITEM', render_kw={'class': 'btn btn-outline-primary-2'})
    update = SubmitField('UPDATE THE ITEM', render_kw={'class': 'btn btn-outline-primary-2'})
    delete = SubmitField('DELETE THE ITEM', render_kw={'class': 'btn btn-outline-primary-2'})