from app import app
from app import routes
from app import db
from app.models import Seller_items
import datetime
import time
import threading

def check_and_update_offers():
    with app.app_context():
        while True:
            current_datetime = datetime.datetime.now().date()
            active_offers = Seller_items.query.filter(
                Seller_items.item_offer_status == 'TO BE ON OFFER'
            ).all()
            for offer in active_offers:
                if offer.item_offer_start_date == current_datetime:
                    offer.item_offer_status = 'ON OFFER'
                if offer.item_offer_end_date < current_datetime:
                    offer.item_offer_status = 'OFFER EXPIRED'
            db.session.commit()
            time.sleep(86400)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    scheduler_thread = threading.Thread(target=check_and_update_offers)
    scheduler_thread.start()

    app.run(debug=True)
