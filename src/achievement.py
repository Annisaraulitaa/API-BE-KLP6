from datetime import datetime
from typing import List
import uuid

from flask_jwt_extended import get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, json, jsonify, request
from src.database import Achievement, AchievementCountry, db
from src.utils.delete_image_from_firebase import delete_image_from_firebase
from src.utils.upload_image_to_firebase import upload_image_to_firebase
from flasgger import swag_from

achievement = Blueprint('achievement', __name__)

@achievement.get('/')
def get_achievements():
    achievements: List[Achievement] = Achievement.query.all()

    return jsonify({
        "data": [a.to_dict() for a in achievements]
    }), http.HTTP_200_OK

@achievement.post('/')
@jwt_required()
def create_achievement():
    created_by = get_jwt_identity()
    title = request.form.get('title', None)
    year = request.form.get('year', None)
    photo = request.files.get('photo', None)
    country = request.form.get('country', None)

    if not title or not year or not photo or not country:
        return jsonify({"msg": "Title, country, year, and photo are required"}), http.HTTP_400_BAD_REQUEST
    
    new_id = str(uuid.uuid4())
    photo_url = upload_image_to_firebase(photo, file_name=f'achievement/{new_id}')
    if not photo_url[0]:
        return jsonify({
            'msg': photo_url[1]
        }), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    created_at = datetime.now().timestamp() * 1000

    achievement = Achievement(
        id=new_id,
        year=int(year),
        photo_url=photo_url[0],
        created_by=created_by,
        updated_at=created_at,
        created_at=created_at
    )

    db.session.add(achievement)

    country = json.loads(country)
    achievement_country_id = str(uuid.uuid4())
    for p in country:
        achievement_country = AchievementCountry(
            id=achievement_country_id,
            achievement_id=achievement.id,
            country=p['country'],
            title=p['title'],
            created_at=created_at,
            updated_at=created_at
        )

        db.session.add(achievement_country)

    db.session.commit()

    return jsonify({
        "msg": "Achievement created successfully",
        "data": achievement.to_dict()
    }), http.HTTP_201_CREATED

@achievement.put('/<achievement_id>')
@jwt_required()
def update_achievement(achievement_id):
    year = request.form.get('year', None)
    photo = request.files.get('photo', None)
    country = request.form.get('country', None)

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
        
        if year: achievement.year = int(year)

        # db.session.commit()

        # remove current achievement country
        AchievementCountry.query.filter_by(achievement_id=achievement.id).delete()
        # db.session.commit()

        # add new achievement country
        if country:
            country = json.loads(country)

            for p in country:
                achievement_country = AchievementCountry(
                    achievement_id=achievement.id,
                    country=p['country'],
                    title=p['title']
                )

                db.session.add(achievement_country)

        db.session.commit()

        return jsonify({
            "msg": "Achievement updated successfully",
            "data": achievement.to_dict()
        }), http.HTTP_200_OK

    return jsonify({"msg": "Achievement not found"}), http.HTTP_404_NOT_FOUND

@achievement.delete('/<achievement_id>')
@jwt_required()
def delete_achievement(achievement_id):
    achievement: Achievement = Achievement.query.get(achievement_id)
    
    if achievement:
        delete = delete_image_from_firebase(achievement.photo_url)

        if not delete[0]:
            return jsonify({"msg": delete[1]}), http.HTTP_500_INTERNAL_SERVER_ERROR
        
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