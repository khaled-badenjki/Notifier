from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from notifier.api.schemas import NotificationSchema
from notifier.models import Notification, Customer
from notifier.extensions import db
from notifier.commons.pagination import paginate


class SmsNotificationResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - notification api
      parameters:
        - in: path
          name: notification_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  notification: NotificationSchema
        404:
          description: notification does not exists
    """

    method_decorators = [jwt_required]

    def get(self, notification_id):
        schema = NotificationSchema(exclude=["type"])
        notification = Notification.query.filter(Notification.type == "sms").get_or_404(
            notification_id
        )
        return {"sms notification": schema.dump(notification)}


class SmsNotificationList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - notification api
      responses:
        200:
          content:
            application/json:
              schema:
                allOf:
                  - $ref: '#/components/schemas/PaginatedResult'
                  - type: object
                    properties:
                      results:
                        type: array
                        items:
                          $ref: '#/components/schemas/NotificationSchema'
    post:
      tags:
        - notification api
      requestBody:
        content:
          application/json:
            schema:
              NotificationSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: sms notification added to queue
                  notification: NotificationSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = NotificationSchema(
            exclude=[
                "type",
            ],
            many=True,
        )
        query = Notification.query
        return paginate(query, schema)

    def post(self):
        # TODO: find out how to remove status field from post request schema docs
        schema = NotificationSchema(
            exclude=[
                "type",
                "status",
            ]
        )
        notification = schema.load(request.json)
        if not Customer.query.get(notification.customer_id):
            return {"error": "customer_id doesn't exist"}, 422
        notification.type = "sms"
        db.session.add(notification)
        db.session.commit()

        return {
            "msg": "sms notification added to queue",
            "notification": schema.dump(notification),
        }, 201
