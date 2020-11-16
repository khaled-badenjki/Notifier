from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError
from notifier.extensions import apispec
from notifier.api.resources import UserResource, UserList, CustomerResource, CustomerList
from notifier.api.schemas import UserSchema, CustomerSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)


api.add_resource(UserResource, "/users/<int:user_id>", endpoint="user_by_id")
api.add_resource(UserList, "/users", endpoint="users")

api.add_resource(CustomerResource, "/customers/<int:customer_id>", endpoint="customer_by_id")
api.add_resource(CustomerList, "/customers", endpoint="customers")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserSchema", schema=UserSchema)
    apispec.spec.components.schema("CustomerSchema", schema=CustomerSchema)

    apispec.spec.path(view=UserResource, app=current_app)
    apispec.spec.path(view=CustomerResource, app=current_app)

    apispec.spec.path(view=UserList, app=current_app)
    apispec.spec.path(view=CustomerList, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    """Return json error for marshmallow validation errors.

    This will avoid having to try/catch ValidationErrors in all endpoints, returning
    correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
    """
    return jsonify(e.messages), 400
