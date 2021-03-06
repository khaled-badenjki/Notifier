from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from notifier.api.schemas import CustomerSchema
from notifier.models import Customer
from notifier.extensions import db
from notifier.commons.pagination import paginate


class CustomerResource(Resource):
    """Single object resource

    ---
    get:
      tags:
        - customer api
      parameters:
        - in: path
          name: customer_id
          schema:
            type: integer
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  customer: CustomerSchema
        404:
          description: customer does not exists
    put:
      tags:
        - customer api
      parameters:
        - in: path
          name: customer_id
          schema:
            type: integer
      requestBody:
        content:
          application/json:
            schema:
              CustomerSchema
      responses:
        200:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: customer updated
                  customer: CustomerSchema
        404:
          description: customer does not exists
    delete:
      tags:
        - customer api
      parameters:
        - in: path
          name: customer_id
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
                    example: customer deleted
        404:
          description: customer does not exists
    """

    method_decorators = [jwt_required]

    def get(self, customer_id):
        schema = CustomerSchema()
        customer = Customer.query.get_or_404(customer_id)
        return {"customer": schema.dump(customer)}

    def put(self, customer_id):
        schema = CustomerSchema(partial=True)
        customer = Customer.query.get_or_404(customer_id)
        customer = schema.load(request.json, instance=customer)
        db.session.commit()

        return {"msg": "customer updated", "customer": schema.dump(customer)}

    def delete(self, customer_id):
        customer = Customer.query.get_or_404(customer_id)
        db.session.delete(customer)
        db.session.commit()

        return {"msg": "customer deleted"}


class CustomerList(Resource):
    """Creation and get_all

    ---
    get:
      tags:
        - customer api
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
                          $ref: '#/components/schemas/CustomerSchema'
    post:
      tags:
        - customer api
      requestBody:
        content:
          application/json:
            schema:
              CustomerSchema
      responses:
        201:
          content:
            application/json:
              schema:
                type: object
                properties:
                  msg:
                    type: string
                    example: customer created
                  customer: CustomerSchema
    """

    method_decorators = [jwt_required]

    def get(self):
        schema = CustomerSchema(many=True)
        query = Customer.query
        return paginate(query, schema)

    def post(self):
        schema = CustomerSchema()
        customer = schema.load(request.json)
        # TODO: handle the logic so that the posted group is not created, but only assigned to the customer
        if Customer.customer_exists(customer.email):
            return {"error": "User with this email already exists"}, 422
        db.session.add(customer)
        db.session.commit()

        return {"msg": "customer created", "customer": schema.dump(customer)}, 201
