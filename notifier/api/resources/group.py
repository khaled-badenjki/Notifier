from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from notifier.api.schemas import GroupSchema
from notifier.models import Group
from notifier.extensions import db
from notifier.commons.pagination import paginate


class GroupResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - group api
      parameters:
        - in: path
          name: group_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  group: GroupSchema
        404:
          description: group does not exists
    """

    method_decorators = [jwt_required]

    def get(self, group_id):
        schema = GroupSchema()
        group = Group.query.get_or_404(group_id)
        return {"group": schema.dump(group)}


class GroupList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - group api
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
                          $ref: '#/components/schemas/GroupSchema'
    post:
      tags:
        - group api
      requestBody:
        content:
          application/json:
            schema:
              GroupSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: group created
                  group: GroupSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = GroupSchema(many=True)
        query = Group.query
        return paginate(query, schema)

    def post(self):
        schema = GroupSchema()
        group = schema.load(request.json)
        db.session.add(group)
        db.session.commit()

        return {"msg": "group created", "group": schema.dump(group)}, 201
