from flask import Blueprint, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import src.constants.http_status_codes as http

token = Blueprint('token', __name__)

@token.post('/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)
    refresh = create_refresh_token(identity=identity)
    return jsonify({
        'access_token': access,
        'refresh_token': refresh,
    }), http.HTTP_200_OK