from notifier.models import Device
from notifier.extensions import ma, db, ma_validate


class DeviceSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    customer_id = ma.Int()
    registration_id = ma.String()
    type = ma.String(validate=ma_validate.OneOf(["ios", "android"]))

    class Meta:
        model = Device
        sqla_session = db.session
        load_instance = True
