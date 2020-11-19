from notifier.extensions import db, db_event
from notifier.tasks import notification
from notifier.models import Customer
import datetime


class Notification(db.Model):
    """Notification model"""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    type = db.Column(db.Enum("sms", "push", name="NotificationTypes"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
    is_dynamic = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "<Notification %s>" % self.id


@db_event.listens_for(Notification, "after_insert")
def after_insert_notification(mapper, connection, target):
    customer = Customer.query.get(target.customer_id)
    if customer and target.type == "sms":
        notification.get_sms_api.delay(
            notification_id=target.id, phone=customer.phone, text=target.text
        )
