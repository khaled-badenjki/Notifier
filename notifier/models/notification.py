from notifier.extensions import db, db_event
import datetime


class Notification(db.Model):
    """Notification model"""

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    status = db.Column(
        db.Enum("processing", "sent", "failed", name="NotificationStatuses"),
        default="processing",
    )
    type = db.Column(db.Enum("sms", "push", name="NotificationTypes"))
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    is_dynamic = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.utcnow
    )

    def __repr__(self):
        return "<Notification %s>" % self.id


@db_event.listens_for(Notification, "after_insert")
def dummy_task(mapper, connection, target):
    print("after_insert", mapper, connection, target)
