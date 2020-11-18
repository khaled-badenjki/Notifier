from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from notifier.extensions import apispec
from notifier.api.resources import (
    UserResource,
    UserList,
    CustomerResource,
    CustomerList,
    GroupResource,
    GroupList,
    DeviceResource,
    DeviceList,
    SmsNotificationResource,
    SmsNotificationList,
)
from notifier.api.schemas import (
    UserSchema,
    CustomerSchema,
    DeviceSchema,
    NotificationSchema,
)

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(
    CustomerResource, "/customers/<int:customer_id>", endpoint="customer_by_id"
)
api.add_resource(CustomerList, "/customers", endpoint="customers")

api.add_resource(GroupResource, "/groups/<int:group_id>", endpoint="group_by_id")
api.add_resource(GroupList, "/groups", endpoint="groups")

api.add_resource(DeviceResource, "/devices/<int:device_id>", endpoint="device_by_id")
api.add_resource(DeviceList, "/devices", endpoint="devices")

api.add_resource(
    SmsNotificationResource,
    "/notifications/sms/<int:notification_id>",
    endpoint="sms_notification_by_id",
)
api.add_resource(
    SmsNotificationList, "/notifications/sms", endpoint="sms_notifications"
)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.components.schema("CustomerSchema", schema=CustomerSchema)
    apispec.spec.components.schema("DeviceSchema", schema=DeviceSchema)
    apispec.spec.components.schema("NotificationSchema", schema=NotificationSchema)

    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=CustomerResource, app=current_app)
    apispec.spec.path(view=GroupResource, app=current_app)
    apispec.spec.path(view=DeviceResource, app=current_app)
    apispec.spec.path(view=SmsNotificationResource, app=current_app)

    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=CustomerList, app=current_app)
    apispec.spec.path(view=GroupList, app=current_app)
    apispec.spec.path(view=DeviceList, app=current_app)
    apispec.spec.path(view=SmsNotificationList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
