from flask import request, jsonify, make_response
from flask_restful import Resource
from models import Product, OrderProduct, Order
from database import db
from utils import customer_required
from collections import defaultdict
from sqlalchemy.exc import IntegrityError
from sqlalchemy import exc

class OrderResource(Resource):
    @customer_required
    def post(self):
        """
        Create a new order
        ---
        tags:
          - Orders
        parameters:
          - in: body
            name: body
            schema:
              type: array
              items:
                type: object
                required:
                  - product_id
                  - quantity
                properties:
                  product_id:
                    type: integer
                  quantity:
                    type: integer
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
        responses:
          201:
            description: Order created
          400:
            description: Failed to create order
        """
        data_list = request.get_json()
        if len(data_list) == 0:
            return make_response(jsonify({'message': 'at least one order needed'}), 400)
        order_list = defaultdict(int)
        for data in data_list:
            product_id = data.get('product_id')
            quantity = data.get('quantity')
            if not isinstance(quantity, int) or quantity <= 0:
                return make_response(jsonify({'message': 'quantity must be a positive integer'}), 400)
            order_list[product_id] += quantity

        updated_products = []
        try:
            # transaction start
            with db.session.begin_nested():
                for product_id, num in order_list.items():
                    product = Product.query.filter_by(id=product_id).with_for_update().first()
                    if product is None:
                        raise ValueError(f'Product with ID {product_id} not found')
                    if product.stock < num:
                        return make_response(jsonify({'message': f'{product.name} is out of stock'}), 400)
                    product.stock -= num
                    updated_products.append(product)
            
            for product in updated_products:
                db.session.add(product)

            user_id = request.headers.get('Authorization')

            new_order = Order(user_id=user_id)
            db.session.add(new_order)
            db.session.commit()

            for product_id, num in order_list.items():
                order_product = OrderProduct(order_id=new_order.id, product_id=product_id, quantity=num)
                db.session.add(order_product)
            db.session.commit()

        except ValueError as ve:
            db.session.rollback()
            return make_response(jsonify({'message': str(ve)}), 400)
        except IntegrityError as ie:
            db.session.rollback()
            return make_response(jsonify({'message': f'IntegrityError: {str(ie)}'}), 500)
        except exc.SQLAlchemyError as se:
            db.session.rollback()
            return make_response(jsonify({'message': f'SQLAlchemyError: {str(se)}'}), 500)
        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({'message': f'Failed to create order: {str(e)}'}), 500)

        return make_response(jsonify({'message': 'Order created'}), 201)
