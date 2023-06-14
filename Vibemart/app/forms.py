# from flask import render_template,request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User, Account
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
    submit = SubmitField('REGISTER')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
        new_user = User(email=email.data, password=self.password.data)
        new_account = Account(email=email.data, password=self.password.data)
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