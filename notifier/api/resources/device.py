from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from notifier.api.schemas import DeviceSchema
from notifier.models import Device
from notifier.extensions import db
from notifier.commons.pagination import paginate


class DeviceResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - device api
      parameters:
        - in: path
          name: device_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  device: DeviceSchema
        404:
          description: device does not exists
    put:
      tags:
        - device api
      parameters:
        - in: path
          name: device_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              DeviceSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: device updated
                  device: DeviceSchema
        404:
          description: device does not exists
    delete:
      tags:
        - device api
      parameters:
        - in: path
          name: device_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: device deleted
        404:
          description: device does not exists
    """

    method_decorators = [jwt_required]

    def get(self, device_id):
        schema = DeviceSchema()
        device = Device.query.get_or_404(device_id)
        return {"device": schema.dump(device)}

    def put(self, device_id):
        schema = DeviceSchema(partial=True)
        device = Device.query.get_or_404(device_id)
        device = schema.load(request.json, instance=device)
        db.session.commit()

        return {"msg": "device updated", "device": schema.dump(device)}

    def delete(self, device_id):
        device = Device.query.get_or_404(device_id)
        db.session.delete(device)
        db.session.commit()

        return {"msg": "device deleted"}


class DeviceList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - device api
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
                          $ref: '#/components/schemas/DeviceSchema'
    post:
      tags:
        - device api
      requestBody:
        content:
          application/json:
            schema:
              DeviceSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: device created
                  device: DeviceSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = DeviceSchema(many=True)
        query = Device.query
        return paginate(query, schema)

    def post(self):
        schema = DeviceSchema()
        device = schema.load(request.json)
        db.session.add(device)
        db.session.commit()

        return {"msg": "device created", "device": schema.dump(device)}, 201
