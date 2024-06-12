from datetime import datetime
import uuid
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, jsonify, request
from src.database import User, db, Admin
from werkzeug.security import check_password_hash, generate_password_hash

from src.utils.delete_image_from_firebase import delete_image_from_firebase
from src.utils.upload_image_to_firebase import upload_image_to_firebase

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
    new_id = str(uuid.uuid4())
    
    new_admin = Admin(
        id=new_id,
        username=username,
        password=generate_password_hash(password),
        created_at=created_at,
        updated_at=created_at
    )

    db.session.add(new_admin)
    db.session.commit()

    return jsonify({
        "msg": "Admin created successfully",
        "data": new_admin.to_dict()
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

@admin.post('/create-user')
@jwt_required()
def create_user():
    name = request.form.get('name', None)
    password = request.form.get('password', None)
    email = request.form.get('email', None)
    phone = request.form.get('phone', None)
    address = request.form.get('address', None)
    photo = request.files.get('photo', None)
    role_id = request.form.get('role_id', None)
    role_text = request.form.get('role_text', None)
    
    if not name or not password or not email or not phone or not address:
        return jsonify({"msg": "All fields must be provided"}), http.HTTP_400_BAD_REQUEST
    
    # save image to firebase storage
    new_id = str(uuid.uuid4())
    photo_url = None

    if photo:
        photo_url = upload_image_to_firebase(photo, file_name=f'photo_profile/{new_id}')
        if not photo_url[0]:
            return jsonify({
                'msg': photo_url[1]
            }), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    if role_id:
        role_id = int(role_id)
    
    admin_id = get_jwt_identity()
    admin: Admin = Admin.query.get(admin_id)

    if admin:
        created_at = datetime.now().timestamp() * 1000
        new_user = User(
            id=new_id,
            name=name,
            password=generate_password_hash(password, method='pbkdf2'),
            email=email,
            phone=phone,
            address=address,
            photo_url=photo_url[0] if photo_url else None,
            role_id=role_id,
            role_text=role_text,
            created_by=admin.id,
            updated_at=created_at,
            created_at=created_at
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "msg": "User created successfully",
            "data": new_user.to_dict()
        }), http.HTTP_201_CREATED

    return jsonify({"msg": "Invalid admin"}), http.HTTP_401_UNAUTHORIZED

@admin.put('/update-user/<user_id>')
@jwt_required()
def update_user(user_id):
    name = request.form.get('name', None)
    email = request.form.get('email', None)
    phone = request.form.get('phone', None)
    address = request.form.get('address', None)
    photo = request.files.get('photo', None)
    role_id = request.form.get('role_id', None)
    role_text = request.form.get('role_text', None)
    
    user: User = User.query.get(user_id)

    if user:
        if photo:
            # save image to firebase storage
            photo_url = upload_image_to_firebase(photo, file_name=f'photo_profile/{user_id}')
            if not photo_url[0]:
                return jsonify({
                    'msg': photo_url[1]
                }), http.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                user.photo_url = photo_url[0]


        if name: user.name = name
        if email: user.email = email
        if phone: user.phone = phone
        if address: user.address = address
        if role_id: user.role_id = role_id
        if role_text: user.role_text = role_text
        user.updated_at = datetime.now().timestamp() * 1000

        db.session.commit()

        return jsonify({
            "msg": "User updated successfully",
            "data": user.to_dict()
        }), http.HTTP_200_OK

    return jsonify({"msg": "User not found"}), http.HTTP_404_NOT_FOUND

@admin.delete('/delete-user/<user_id>')
@jwt_required()
def delete_user(user_id):
    user: User = User.query.get(user_id)

    if user:
        if user.photo_url:
            delete = delete_image_from_firebase(user.photo_url)

            if not delete[0]:
                return jsonify({"msg": delete[1]}), http.HTTP_500_INTERNAL_SERVER_ERROR

        db.session.delete(user)
        db.session.commit()

        return jsonify({"msg": "User deleted successfully"}), http.HTTP_200_OK

    return jsonify({"msg": "User not found"}), http.HTTP_404_NOT_FOUND

# a function that will create one default admin and will be called when the app is first run
def create_default_admin():
    admin = Admin.query.filter_by(username="admin").first()
    if not admin:
        created_at = datetime.now().timestamp() * 1000
        new_id = str(uuid.uuid4())
        new_admin = Admin(
            id=new_id,
            username="admin",
            password=generate_password_hash("admin", method='pbkdf2'),
            created_at=created_at,
            updated_at=created_at
        )
        db.session.add(new_admin)
        db.session.commit()
        print("Default admin created successfully")
    else:
        print("Default admin already exists")