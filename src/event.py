from datetime import datetime
import uuid
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Event, db
import src.constants.http_status_codes as http
from src.utils.upload_image_to_firebase import upload_image_to_firebase
from src.utils.delete_image_from_firebase import delete_image_from_firebase

event = Blueprint('event', __name__)

@event.get('/')
def get_all():

    events = Event.query.all()
    
    return jsonify([event.to_dict() for event in events]), http.HTTP_200_OK

@event.get('/<id>')
def get_by_id(id):
    event = Event.query.filter_by(id=id).first()
    
    if not event:
        return jsonify({"msg": "Event not found"}), http.HTTP_404_NOT_FOUND
    
    return jsonify(event.to_dict()), http.HTTP_200_OK

@event.post('/')
@jwt_required()
def create():
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    photo = request.files.get('photo', None)
    created_by = get_jwt_identity()
    
    if not title or not content or not photo:
        return jsonify({"msg": "All fields must be provided"}), http.HTTP_400_BAD_REQUEST
    
    new_id = str(uuid.uuid4())
    photo_url = upload_image_to_firebase(photo, file_name=f'event/{new_id}')
    if not photo_url[0]:
        return jsonify({
            'msg': photo_url[1]
        }), http.HTTP_500_INTERNAL_SERVER_ERROR

    created_at = datetime.now().timestamp() * 1000   

    event = Event(
        id=new_id,
        title=title,
        content=content,
        photo_url=photo_url[0],
        created_by=created_by,
        updated_at=created_at,
        created_at=created_at
    )
    
    db.session.add(event)
    db.session.commit()
    
    return jsonify(event.to_dict()), http.HTTP_201_CREATED

@event.put('/<id>')
def update(id):
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    photo = request.form.get('photo', None)
    
    event: Event = Event.query.get(id)
    
    if not event:
        return jsonify({"msg": "Event not found"}), http.HTTP_404_NOT_FOUND
    
    if title:
        event.title = title
    if content:
        event.content = content
    if photo:
        photo_url = upload_image_to_firebase(photo, file_name=f'event/{id}')
        if not photo_url[0]:
            return jsonify({
                'msg': photo_url[1]
            }), http.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            event.photo_url = photo_url[0]
    
    event.updated_at = datetime.now().timestamp() * 1000
    
    db.session.commit()
    
    return jsonify(event.to_dict()), http.HTTP_200_OK

@event.delete('/<id>')
def delete(id):
    event: Event = Event.query.get(id)
    
    if not event:
        return jsonify({"msg": "Event not found"}), http.HTTP_404_NOT_FOUND
    
    delete = delete_image_from_firebase(event.photo_url)

    if not delete[0]:
        return jsonify({"msg": delete[1]}), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    db.session.delete(event)
    db.session.commit()
    
    return jsonify({"msg": "Event deleted"}), http.HTTP_200_OK