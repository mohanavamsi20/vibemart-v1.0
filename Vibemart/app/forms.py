from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('signin-email', validators=[InputRequired(), Length(min=4, max=120)], attributes={'placeholder': 'Username or email address *', 'class': 'form-control', 'id': 'signin-email'})
    password = PasswordField('signin-password', validators=[InputRequired(), Length(min=4, max=60)])
    submit = SubmitField('login')

class RegisterForm(FlaskForm):
    email = StringField('register-email', validators=[InputRequired(), Length(min=4, max=120)])
    password = PasswordField('register-password', validators=[InputRequired(), Length(min=4, max=60)])
    submit = SubmitField('register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')

