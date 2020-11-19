from notifier.models import Notification
from notifier.extensions import ma, db


class ParameterSchema(ma.Schema):

    key = ma.String()
    value = ma.String()


class NotificationSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    text = ma.String(required=True)
    customer_id = ma.Int(required=False)
    group_id = ma.Int(required=False)
    is_dynamic = ma.Bool(default=False, required=True)
    extra_params = ma.List(ma.Nested(ParameterSchema), required=False)

    class Meta:
        model = Notification
        sqla_session = db.session
        load_instance = True
        exclude = (
            "type",
            "created_at",
            "updated_at",
        )
