from flask import request, jsonify
from flask_restful import Resource
from models import User
from services.cache_service import app_cache

class LoginResource(Resource):
    def post(self):
        """
        User Login
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
              properties:
                username:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Successful login
          400:
            description: Invalid credentials
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not user.check_password(password):
            return {"message": "Invalid credentials"}, 400
        login_user = "Customer" if user.permission == 0 else "Manager"
        token = str(user.id)
        app_cache.add_user(token, user)
        return jsonify({"message": f"{login_user} Login successful!", "token": token})
