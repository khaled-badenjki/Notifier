from notifier.models import Notification
from notifier.extensions import ma, db, ma_validate


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    text = ma.String(required=True)
    customer_id = ma.Int(required=True)
    is_dynamic = ma.Bool(default=False)
    status = ma.String(validate=ma_validate.OneOf(["processing", "sent", "failed",]))

    class Meta:
        model = Notification
        sqla_session = db.session
        load_instance = True
        exclude = ("type", "created_at", "updated_at",)
