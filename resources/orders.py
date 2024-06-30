from flask import request, jsonify, make_response
from flask_restful import Resource
from models import Product, OrderProduct, Order
from database import db
from utils import login_required
from collections import defaultdict
from services.cache_service import app_cache

class OrdersResource(Resource):
    @login_required
    def get(self):
        """
        Get order list.
        If you are a customer, you will get your orders only.
        If you are a manager, you could get all orders that created by customers. 
        ---
        tags:
          - Orders
        parameters:
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
          - name: order_id
            in: query
            required: false
            type: integer
          - name: product_id
            in: query
            required: false
            type: integer
        responses:
          200:
            description: order list
            schema:
              type: array
              items:
                type: object
                properties:
                  order_id:
                    type: integer
                  user_id:
                    type: integer
                  products:
                    type: array
                    items:
                      type: object
                      properties:
                        product_id:
                          type: integer
                        product_name:
                          type: string
                        quantity:
                          type: integer
          404:
            description: Order not found
        """
        user_id = request.headers.get('Authorization')
        order_id = request.args.get("order_id", None)
        product_id = request.args.get("product_id", None)
        query = None

        if app_cache.is_user_manager(user_id):
            query = db.session.query(Order, Product, OrderProduct).\
                join(OrderProduct, Order.id == OrderProduct.order_id).\
                join(Product, Product.id == OrderProduct.product_id)
        elif app_cache.is_user_customer(user_id):
            query = db.session.query(Order, Product, OrderProduct).\
                join(OrderProduct, Order.id == OrderProduct.order_id).\
                join(Product, Product.id == OrderProduct.product_id).\
                filter(Order.user_id == user_id)
        else:
            return make_response(jsonify({'message': 'User role not recognized'}), 403)

        if order_id is not None:
            query = query.filter(Order.id == order_id)

        if product_id is not None:
            query = query.filter(Product.id == product_id)

        join_list = query.all()

        if not join_list:
            return make_response(jsonify({'message': 'Order not found'}), 404)

        orders = defaultdict(lambda: {'order_id': None, 'user_id': None, 'products': []})

        for order, product, order_product in join_list:
            if orders[order.id]['order_id'] is None:
                orders[order.id]['order_id'] = order.id
                orders[order.id]['user_id'] = order.user_id
            orders[order.id]['products'].append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': order_product.quantity
            })

        result = list(orders.values())

        return make_response(jsonify(result), 200)