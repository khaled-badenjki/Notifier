from notifier.extensions import db


class Device(db.Model):
    """Device model for push notifications"""

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"),
                            nullable=False)
    registration_id = db.Column(db.String(512), nullable=True)
    type = db.Column(db.Enum("android", "ios", name="DeviceTypes"), nullable=False)
    version = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<Device %s>" % self.type
