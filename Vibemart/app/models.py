from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
from app import db

class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.email}')"

    
class Account(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    firstname=db.Column(db.String(120))
    lastname=db.Column(db.String(120))
    displayname=db.Column(db.String(120))
    email=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(120))
    address_line1=db.Column(db.String(120))
    address_line2=db.Column(db.String(120))
    city=db.Column(db.String(120))
    state=db.Column(db.String(120))
    zipcode=db.Column(db.String(120))
    country=db.Column(db.String(120))
    phone=db.Column(db.String(120))

    def __repr__(self):
        return f"Account('{self.firstname}','{self.lastname}','{self.displayname}','{self.email}','{self.password}')"

class Seller_items(db.Model):
    item_id= db.Column(db.Integer, primary_key=True)
    seller_id=db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    item_name=db.Column(db.String(120))
    item_price=db.Column(db.Integer)
    item_description=db.Column(db.String(120))
    item_image=db.Column(db.String(120))
    item_image_file_name=db.Column(db.String(120))
    item_category=db.Column(db.String(120))
    item_current_status=db.Column(db.String(120))
    item_quantity=db.Column(db.Integer)
    item_offer_percentage=db.Column(db.Integer)
    item_offer_price=db.Column(db.Integer)
    item_offer_start_date=db.Column(db.Date)
    item_offer_end_date=db.Column(db.Date)
    item_offer_status=db.Column(db.String(120))

    def __repr__(self):
        return f"Seller_items('{self.item_name}','{self.item_price}','{self.item_description}','{self.item_image}','{self.item_category}','{self.item_current_status}','{self.item_quantity}','{self.item_offer_percentage}','{self.item_offer_price}','{self.item_offer_start_date}','{self.item_offer_end_date}','{self.item_offer_status}')"


class Cart(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    buyyer_id=db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    seller_id=db.Column(db.Integer, db.ForeignKey('seller_items.seller_id'), nullable=False)
    item_id=db.Column(db.Integer, db.ForeignKey('seller_items.item_id'), nullable=False)
    item_name=db.Column(db.String(120))
    item_quantity=db.Column(db.Integer)
    item_category=db.Column(db.String(120))
    item_price=db.Column(db.Integer)
    item_total_price=db.Column(db.Integer)
    item_status=db.Column(db.String(120))

    def __repr__(self):
        return f"Cart('{self.user_id}','{self.item_id}','{self.item_quantity}','{self.item_price}','{self.item_total_price}','{self.item_status}')"