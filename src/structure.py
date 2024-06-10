from typing import List
import src.constants.http_status_codes as http
from flask import Blueprint, jsonify
from src.database import User

structure = Blueprint('structure', __name__)

@structure.get('/')
def get_structure():
    # get all users with role_id not null
    users: List[User] = User.query.filter(User.role_id != None).all()

    # sort users by role_id
    users.sort(key=lambda x: x.role_id)

    # return users
    return jsonify({
        "data": [user.to_dict() for user in users]
    }), http.HTTP_200_OK