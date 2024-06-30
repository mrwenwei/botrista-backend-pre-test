from flask import request, jsonify, make_response
from flask_restful import Resource
from models import Product, OrderProduct
from database import db
from utils import login_required, manager_required

class ProductResource(Resource):
    @login_required
    def get(self):
        """
        Get a product by ID
        ---
        tags:
          - Products
        parameters:
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
          - name: product_id
            in: query
            required: true
            type: integer
        responses:
          200:
            description: A single product
            schema:
              id: Product
              properties:
                id:
                  type: integer
                name:
                  type: string
                price:
                  type: number
                stock:
                  type: integer
          404:
            description: Product not found
        """
        product_id = request.args.get("product_id", None)
        if product_id is None:
            return {"message": "product_id is required"}, 400
        product = Product.query.get_or_404(product_id)
        return jsonify({
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "stock": product.stock
        })

    @manager_required
    def post(self):
        """
        Create a new product
        ---
        tags:
          - Products
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - name
                - price
                - stock
              properties:
                name:
                  type: string
                price:
                  type: number
                stock:
                  type: integer
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
        responses:
          201:
            description: Product created
          400:
            description: Product already exists
        """
        data = request.get_json()
        name = data.get('name')
        price = data.get('price')
        stock = data.get('stock')

        if Product.query.filter_by(name=name).first():
            return {"message": "Product already exists"}, 400
        
        new_product = Product(name=name, price=price, stock=stock)
        db.session.add(new_product)
        db.session.commit()
        return make_response(jsonify({"message": f"Product created, id:{new_product.id}"}), 201)

    @manager_required
    def put(self):
        """
        Update a product by ID
        ---
        tags:
          - Products
        parameters:
          - name: product_id
            in: query
            required: true
            type: integer
          - in: body
            name: body
            schema:
              type: object
              properties:
                name:
                  type: string
                price:
                  type: number
                stock:
                  type: integer
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
        responses:
          200:
            description: Product updated
          404:
            description: Product not found
        """
        product_id = request.args.get("product_id", None)
        if product_id is None:
            return {"message": "product_id is required"}, 400
        product = Product.query.get_or_404(product_id)
        data = request.get_json()
        product.name = data.get('name', product.name)
        product.price = data.get('price', product.price)
        product.stock = data.get('stock', product.stock)
        db.session.commit()
        return make_response(jsonify({"message": "Product updated"}), 200)

    @manager_required
    def delete(self):
      """
      Delete a product by ID
      ---
      tags:
        - Products
      parameters:
        - name: product_id
          in: query
          required: true
          type: integer
        - in: header
          name: Authorization
          type: string
          required: True
      responses:
        200:
          description: Product deleted
        404:
          description: Product not found
        400:
          description: Bad request
        409:
          description: Product cannot be deleted because it is referenced in an order
      """
      product_id = request.args.get("product_id", None)
      if product_id is None:
          return {"message": "product_id is required"}, 400

      # Check if the product exists in OrderProduct table
      order_product_count = db.session.query(OrderProduct).filter_by(product_id=product_id).count()
      if order_product_count > 0:
          return make_response(jsonify({"message": "Product cannot be deleted because it is referenced in an order"}), 409)

      product = Product.query.get_or_404(product_id)
      db.session.delete(product)
      db.session.commit()
      return make_response(jsonify({"message": "Product deleted"}), 200)
