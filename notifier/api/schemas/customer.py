from notifier.models import Customer
from notifier.extensions import ma, db
from notifier.api.schemas.group import GroupSchema


class CustomerSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    groups = ma.Nested(GroupSchema, many=True)

    class Meta:
        model = Customer
        sqla_session = db.session
        load_instance = True
