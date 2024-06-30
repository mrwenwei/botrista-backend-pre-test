from flask import request, jsonify, make_response
from flask_restful import Resource
from models import User
from database import db

class SignupResource(Resource):
    def post(self):
        """
        User Signup
        ---
        tags:
          - Auth
        parameters:
          - in: body
            name: body
            schema:
              type: object
              required:
                - username
                - password
                - permission
              properties:
                username:
                  type: string
                password:
                  type: string
                permission:
                  description: 0 is customer, 1 is manager
                  type: integer
        responses:
          201:
            description: User created
          400:
            description: User already exists
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        permission = data.get('permission')

        if User.query.filter_by(username=username).first():
            return make_response(jsonify({"message": "User already exists"}), 400)

        if permission not in {0, 1}:
            return make_response(jsonify({"message": "Wrong permission"}), 400)

        new_user = User(username=username)
        new_user.set_password(password)
        new_user.set_permission(permission)
        db.session.add(new_user)
        db.session.commit()

        return make_response(jsonify({"message": "User created"}), 201)
