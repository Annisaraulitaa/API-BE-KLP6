from datetime import datetime
from typing import List
import uuid

from flask_jwt_extended import get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, json, jsonify, request
from src.database import Achievement, AchievementCountry, db
from src.utils.upload_image_to_firebase import upload_image_to_firebase
from flasgger import swag_from

achievement = Blueprint('achievement', __name__)

@achievement.get('/')
def get_achievements():
    achievements: List[Achievement] = Achievement.query.all()

    return jsonify({
        "data": [a.to_dict() for a in achievements]
    }), http.HTTP_200_OK

@achievement.post('/create')
@jwt_required()
def create_achievement():
    created_by = get_jwt_identity()
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    year = request.form.get('year', None)
    photo = request.form.get('photo', None)
    place = request.form.get('place', None)

    if not title or not content or not year or not photo:
        return jsonify({"msg": "Title, content, year, and photo are required"}), http.HTTP_400_BAD_REQUEST
    
    new_id = str(uuid.uuid4())
    photo_url = upload_image_to_firebase(photo, file_name=f'achievement/{new_id}')
    if not photo_url[0]:
        return jsonify({
            'msg': photo_url[1]
        }), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    created_at = datetime.now().timestamp() * 1000

    achievement = Achievement(
        id=new_id,
        content=content,
        year=year,
        photo_url=photo_url,
        created_by=created_by,
        updated_at=created_at,
        created_at=created_at
    )

    db.session.add(achievement)
    db.session.commit()

    place = json.loads(place)

    for p in place:
        achievement_country = AchievementCountry(
            achievement_id=achievement.id,
            country=p['country'],
            place=p['title']
        )

        db.session.add(achievement_country)
        db.session.commit()

    return jsonify({
        "msg": "Achievement created successfully",
        "data": achievement.to_dict()
    }), http.HTTP_201_CREATED

@achievement.put('/update/<achievement_id>')
@jwt_required()
def update_achievement(achievement_id):
    content = request.form.get('content', None)
    year = request.form.get('year', None)
    photo = request.form.get('photo', None)
    place = request.form.get('place', None)

    achievement: Achievement = Achievement.query.get(achievement_id)
    
    if achievement:
        if photo:
            # save image to firebase storage
            photo_url = upload_image_to_firebase(photo, file_name=f'achievement/{achievement_id}')
            if not photo_url[0]:
                return jsonify({
                    'msg': photo_url[1]
                }), http.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                achievement.photo_url = photo_url[0]
        
        if content: achievement.content = content
        if year: achievement.year = year

        db.session.commit()

        # remove current achievement country
        AchievementCountry.query.filter_by(achievement_id=achievement.id).delete()
        db.session.commit()

        # add new achievement country
        place = json.loads(place)

        for p in place:
            achievement_country = AchievementCountry(
                achievement_id=achievement.id,
                country=p['country'],
                place=p['title']
            )

            db.session.add(achievement_country)
            db.session.commit()

        return jsonify({
            "msg": "Achievement updated successfully",
            "data": achievement.to_dict()
        }), http.HTTP_200_OK

    return jsonify({"msg": "Achievement not found"}), http.HTTP_404_NOT_FOUND

@achievement.delete('/delete/<achievement_id>')
@jwt_required()
def delete_achievement(achievement_id):
    achievement: Achievement = Achievement.query.get(achievement_id)
    
    if achievement:
        db.session.delete(achievement)
        db.session.commit()

        return jsonify({
            "msg": "Achievement deleted successfully",
            "data": achievement.to_dict()
        }), http.HTTP_200_OK

    return jsonify({"msg": "Achievement not found"}), http.HTTP_404_NOT_FOUND

@achievement.get('/<achievement_id>')
def get_achievement(achievement_id):
    achievement: Achievement = Achievement.query.get(achievement_id)
    
    if achievement:
        return jsonify({
            "data": achievement.to_dict()
        }), http.HTTP_200_OK

    return jsonify({"msg": "Achievement not found"}), http.HTTP_404_NOT_FOUND