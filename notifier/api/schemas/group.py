from notifier.models import Group
from notifier.extensions import ma, db


class GroupSchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)

    class Meta:
        model = Group
        sqla_session = db.session
        load_instance = True
