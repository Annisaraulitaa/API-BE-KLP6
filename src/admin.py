from datetime import datetime
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, jsonify, request
from src.database import db, Admin
from werkzeug.security import check_password_hash, generate_password_hash

admin = Blueprint('admin', __name__)

@admin.post('/login')
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Username and password must be provided"}), http.HTTP_400_BAD_REQUEST
    
    admin: Admin = Admin.query.filter_by(username=username).first()

    if admin:
        if check_password_hash(admin.password, password):
            refresh=create_refresh_token(identity=admin.id)
            access=create_access_token(identity=admin.id)
            return jsonify({
                "msg": "Login successful",
                "refresh_token": refresh,
                "access_token": access,
                "admin": admin.to_dict()
            }), http.HTTP_201_CREATED

    return jsonify({"msg": "Invalid username or password"}), http.HTTP_401_UNAUTHORIZED

@admin.post('/register')
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    
    if not username or not password:
        return jsonify({"msg": "Username and password must be provided"}), http.HTTP_400_BAD_REQUEST
    
    admin: Admin = Admin.query.filter_by(username=username).first()

    if admin:
        return jsonify({"msg": "Username already exists"}), http.HTTP_409_CONFLICT

    created_at = datetime.now().timestamp() * 1000
    
    new_admin = Admin(
        username=username,
        password=generate_password_hash(password),
        created_at=created_at,
        updated_at=created_at
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "msg": "Admin created successfully",
        "admin": new_admin.to_dict()
    }), http.HTTP_201_CREATED

@admin.put('/change-password')
@jwt_required()
def change_password():
    current_password = request.json.get('current_password', None)
    new_password = request.json.get('new_password', None)
    
    if not current_password or not new_password:
        return jsonify({"msg": "Current password and new password must be provided"}), http.HTTP_400_BAD_REQUEST
    
    admin_id = get_jwt_identity()
    admin: Admin = Admin.query.get(admin_id)

    if admin:
        if check_password_hash(admin.password, current_password):
            admin.password = generate_password_hash(new_password)
            db.session.commit()
            return jsonify({"msg": "Password changed successfully"}), http.HTTP_200_OK

    return jsonify({"msg": "Invalid current password"}), http.HTTP_401_UNAUTHORIZED