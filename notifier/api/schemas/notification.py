from notifier.models import Notification
from notifier.extensions import ma, db, ma_validate


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    text = ma.String()
    customer_id = ma.Int()
    is_dynamic = ma.Bool()
    type = ma.String(validate=ma_validate.OneOf(["push", "sms"]))

    class Meta:
        model = Notification
        sqla_session = db.session
        load_instance = True
