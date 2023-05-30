from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:33535@localhost:3306/vibemart'
app.config['SECRET_KEY'] = 'thisissecretkey'
db = SQLAlchemy(app)

from app.models import User
with app.app_context():
    db.create_all()


csrf = CSRFProtect(app)

from app import routes