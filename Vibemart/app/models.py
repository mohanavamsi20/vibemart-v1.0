from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from app import db

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"

    
# class Account(db.Model):
#     firstname=db.Column(db.String(120))
#     lastname=db.Column(db.String(120))
#     displayname=db.Column(db.String(120))
#     email=db.Column(db.String(120), unique=True, nullable=False)
#     password=db.Column(db.String(60), nullable=False)

#     def __repr__(self):
#         return f"Account('{self.firstname}','{self.lastname}','{self.displayname}','{self.email}','{self.password}')"


