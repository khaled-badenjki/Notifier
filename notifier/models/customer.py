from notifier.extensions import db


class Customer(db.Model):
    """Customer model for notifications"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    language = db.Column(db.String(30), default='ar', nullable=True)

    def __repr__(self):
        return "<Customer %s>" % self.name

    @staticmethod
    def customer_exists(email):
        return Customer.query.filter(Customer.email == email).first() is not None
