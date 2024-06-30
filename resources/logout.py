from flask import request, jsonify
from flask_restful import Resource
from services.cache_service import app_cache

class LogoutResource(Resource):
    def post(self):
        """
        User Logout
        ---
        tags:
          - Auth
        parameters:
          - in: header
            name: Authorization
            type: string
            required: True
            description: token (user_id) for the logged-in user
        responses:
          200:
            description: Successful logout
          401:
            description: Invalid credentials
        """
        token = request.headers.get('Authorization')
        app_cache.remove_user(token)
        return jsonify({"message": "Logout successful"})
