from datetime import datetime
import uuid
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Gallery, db
import src.constants.http_status_codes as http
from src.utils.upload_image_to_firebase import upload_image_to_firebase

gallery = Blueprint('gallery', __name__)

@gallery.get('/')
def get_gallery():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = Gallery.query.paginate(page, per_page, False)
    gallery_items = pagination.items
    
    return jsonify({
        "data": [g.to_dict() for g in gallery_items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), http.HTTP_200_OK

@gallery.get('/<gallery_id>')
def get_gallery_by_id(gallery_id):
    gallery: Gallery = Gallery.query.filter_by(id=gallery_id).first()
    
    if gallery:
        return jsonify({
            "data": gallery.to_dict()
        }), http.HTTP_200_OK
    
    return jsonify({"msg": "Gallery not found"}), http.HTTP_404_NOT_FOUND

@gallery.post('/create')
@jwt_required()
def create_gallery():
    created_by = get_jwt_identity()
    title = request.form.get('title', None)
    photo = request.form.get('photo', None)
    
    if not title or not photo:
        return jsonify({"msg": "Title and photo are required"}), http.HTTP_400_BAD_REQUEST
    
    new_id = str(uuid.uuid4())
    photo_url = upload_image_to_firebase(photo, file_name=f'gallery/{new_id}')
    if not photo_url[0]:
        return jsonify({
            'msg': photo_url[1]
        }), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    created_at = datetime.now().timestamp() * 1000

    gallery = Gallery(
        id=new_id,
        title=title,
        photo_url=photo_url,
        created_by=created_by,
        updated_at=created_at,
        created_at=created_at
    )

    db.session.add(gallery)
    db.session.commit()

    return jsonify({
        "msg": "Gallery created",
        "data": gallery.to_dict()
    }), http.HTTP_201_CREATED

@gallery.put('/update/<gallery_id>')
@jwt_required()
def update_gallery(gallery_id):
    title = request.form.get('title', None)
    photo = request.form.get('photo', None)
    
    gallery: Gallery = Gallery.query.get(gallery_id)
    
    if gallery:
        if photo:
            photo_url = upload_image_to_firebase(photo, file_name=f'gallery/{gallery_id}')
            if not photo_url[0]:
                return jsonify({
                    'msg': photo_url[1]
                }), http.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                gallery.photo_url = photo_url[0]
        
        if title: gallery.title = title
        gallery.updated_at = datetime.now().timestamp() * 1000

        db.session.commit()

        return jsonify({
            "msg": "Gallery updated",
            "data": gallery.to_dict()
        }), http.HTTP_200_OK
    
    return jsonify({"msg": "Gallery not found"}), http.HTTP_404_NOT_FOUND

@gallery.delete('/delete/<gallery_id>')
@jwt_required()
def delete_gallery(gallery_id):
    gallery: Gallery = Gallery.query.get(gallery_id)
    
    if gallery:
        db.session.delete(gallery)
        db.session.commit()
        
        return jsonify({"msg": "Gallery deleted"}), http.HTTP_200_OK
    
    return jsonify({"msg": "Gallery not found"}), http.HTTP_404_NOT_FOUND