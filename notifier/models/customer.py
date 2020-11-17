from notifier.extensions import db


customer_group = db.Table(
    "customer_group",
    db.Column(
        "customer_id", db.Integer, db.ForeignKey("customer.id"), primary_key=True
    ),
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
)


class Customer(db.Model):
    """Customer model for notifications"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.String(30), unique=True, nullable=False)
    language = db.Column(db.String(30), default="ar", nullable=True)
    groups = db.relationship(
        "Group",
        secondary=customer_group,
        lazy="subquery",
        backref=db.backref("group_customers", lazy=True),
    )

    def __repr__(self):
        return "<Customer %s>" % self.name

    @staticmethod
    def customer_exists(email):
        return Customer.query.filter(Customer.email == email).first() is not None


class Group(db.Model):
    """Group model for group notifications"""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    customers = db.relationship(
        "Customer",
        secondary=customer_group,
        lazy="subquery",
        backref=db.backref("customer_groups", lazy=True),
    )

    def __repr__(self):
        return "<Group %s>" % self.name
