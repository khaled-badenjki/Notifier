from notifier.models import Device
from notifier.extensions import ma, db


class DeviceSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Device
        sqla_session = db.session
        load_instance = True
