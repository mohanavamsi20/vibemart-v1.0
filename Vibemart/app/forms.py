# from flask import session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User
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
        # new_account = Account(email=email.data, password=self.password.data)
        # db.session.add(new_account)
        db.session.add(new_user)
        db.session.commit()
        

# class AcccountForm(FlaskForm):
#     if 'user_id' in session:
#         firstname = StringField('firstname', validators=[InputRequired(), Length(min=4, max=120)], value=db.firstname(session.get('user_id')))
#         lastname = StringField('lastname', validators=[InputRequired(), Length(min=4, max=120)], value=db.lastname(session.get('user_id')))
#         email = StringField('email', validators=[InputRequired(), Length(min=4, max=120)], value=session.get('user_id'), readonly=True)
#         current_password = PasswordField('password', validators=[Length(min=4, max=60)])
#         new_password = PasswordField('new_password', validators=[Length(min=4, max=60)])
#         confirm_password = PasswordField('confirm_password', validators=[Length(min=4, max=60)])
#         submit = SubmitField('SAVE CHANGERS')

#         if(current_password.data == db.password(session.get('user_id'))):
#             if(new_password.data == confirm_password.data):
#                 db.update_password(session.get('user_id'), new_password.data)
#             else:
#                 raise ValidationError('Passwords do not match')
#         else:
#             raise ValidationError('Password is incorrect')