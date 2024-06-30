from flask import jsonify, make_response, request
from flask_restful import Resource
from sqlalchemy import and_
from models import Product
from utils import login_required
from database import db

class ProductsResource(Resource):
    @login_required
    def get(self):
        """
        Get all products
        ---
        tags:
          - Products
        parameters:
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
          - name: price_lower_bound
            in: query
            required: false
            type: number
          - name: price_upper_bound
            in: query
            required: false
            type: number
          - name: stock_lower_bound
            in: query
            required: false
            type: integer
          - name: stock_upper_bound
            in: query
            required: false
            type: integer
        responses:
          200:
            description: A list of products
            schema:
              type: array
              items:
                $ref: '#/definitions/Product'
        """
        query = db.session.query(Product)
        filters = []
    
        price_lower_bound = request.args.get("price_lower_bound", None)
        price_upper_bound = request.args.get("price_upper_bound", None)
        stock_lower_bound = request.args.get("stock_lower_bound", None)
        stock_upper_bound = request.args.get("stock_upper_bound", None)
        if price_lower_bound:
            filters.append(Product.price >= price_lower_bound)
        if price_upper_bound:
            filters.append(Product.price <= price_upper_bound)
        if stock_lower_bound:
            filters.append(Product.stock >= stock_lower_bound)
        if stock_upper_bound:
            filters.append(Product.stock <= stock_upper_bound)
        
        if filters:
            query = query.filter(and_(*filters))
        products = query.all()
        products_res = []
        for product in products:
            product_dict = {
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'stock': product.stock
            }
            products_res.append(product_dict)
        
        return make_response(jsonify(products_res), 200)
