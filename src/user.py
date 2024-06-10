from datetime import datetime
import uuid
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, jsonify, request
from src.database import User, db, Admin
from werkzeug.security import check_password_hash, generate_password_hash

from src.utils.upload_image_to_firebase import upload_image_to_firebase

user = Blueprint('user', __name__)

@user.post('/login')
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Username and password must be provided"}), http.HTTP_400_BAD_REQUEST
    
    user: User = User.query.filter_by(username=username).first()

    if user:
        if check_password_hash(user.password, password):
            refresh=create_refresh_token(identity=user.id)
            access=create_access_token(identity=user.id)
            return jsonify({
                "msg": "Login successful",
                "refresh_token": refresh,
                "access_token": access,
                "user": user.to_dict()
            }), http.HTTP_201_CREATED

    return jsonify({"msg": "Invalid username or password"}), http.HTTP_401_UNAUTHORIZED

@user.put('/update')
@jwt_required()
def update():
    user_id = get_jwt_identity()
    user: User = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), http.HTTP_404_NOT_FOUND
    
    name = request.form.get('name', None)
    old_password = request.form.get('password', None)
    new_password = request.form.get('new_password', None)
    email = request.form.get('email', None)
    phone = request.form.get('phone', None)
    address = request.form.get('address', None)
    photo = request.form.get('photo', None)
    
    if name:
        user.name = name
    if old_password and new_password:
        if check_password_hash(user.password, old_password):
            user.password = generate_password_hash(new_password)
        else:
            return jsonify({"msg": "Invalid password"}), http.HTTP_401_UNAUTHORIZED
    if email:
        user.email = email
    if phone:
        user.phone = phone
    if address:
        user.address = address
    if photo:
        photo_url = upload_image_to_firebase(photo, file_name=f'photo_profile/{user_id}')
        if not photo_url[0]:
            return jsonify({
                'msg': photo_url[1]
            }), http.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            user.photo_url = photo_url[0]
    
    user.updated_at = datetime.now().timestamp() * 1000
    
    db.session.commit()
    
    return jsonify({"msg": "User updated", "data": user.to_dict()}), http.HTTP_200_OK

@user.get('/profile')
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user: User = User.query.filter_by(id=user_id).first()
    
    if user:
        return jsonify({"data": user.to_dict()}), http.HTTP_200_OK
    
    return jsonify({"msg": "User not found"}), http.HTTP_404_NOT_FOUND