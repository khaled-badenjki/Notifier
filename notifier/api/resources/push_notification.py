from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from notifier.api.schemas import NotificationSchema
from notifier.models import Notification, Customer, Group
from notifier.extensions import db
from notifier.commons.pagination import paginate


class PushNotificationResource(Resource):
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
        notification = Notification.query.filter(
            Notification.type == "push"
        ).get_or_404(notification_id)
        return {"push notification": schema.dump(notification)}


class PushNotificationList(Resource):
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
                    example: push notification added to queue
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
        schema = NotificationSchema(
            exclude=[
                "type",
            ]
        )
        notification = schema.load(request.json)
        if notification.group_id:
            group = Group.query.get_or_404(notification.group_id)
            customers = group.group_customers
            for customer in customers:
                db.session.add_all(
                    [
                        Notification(
                            customer_id=customer.id,
                            type="push",
                            text=notification.text,
                            group_id=notification.group_id,
                            is_dynamic=notification.is_dynamic,
                        )
                    ]
                )
                db.session.flush()
            db.session.commit()
            return {
                "msg": "push group notifications added to queue",
            }, 201
        if not Customer.query.get(notification.customer_id):
            return {"error": "customer_id doesn't exist"}, 422
        notification.type = "push"
        db.session.add(notification)
        db.session.commit()

        return {
            "msg": "push notification added to queue",
            "notification": schema.dump(notification),
        }, 201
