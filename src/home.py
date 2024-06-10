from typing import List
from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.database import Gallery, News, AchievementCountry, User, db
import src.constants.http_status_codes as http



home = Blueprint('home', __name__)

@home.get('/')
def get_home():
    gallery: List[Gallery] = Gallery.query.limit(4).all()
    gallery_data = [g.to_dict() for g in gallery]

    news: List[News] = News.query.limit(2).all()
    news_data = [n.to_dict() for n in news]

    achievement_country: List[AchievementCountry] = AchievementCountry.query.all()
    # count for every title they have
    achievement_count = len(achievement_country)
    # create count for every different country
    country_count = len(set([ac.country for ac in achievement_country]))
    # count how many users are there
    user_count = User.query.count()
    # user_count: List[User] = User.query.all()

    return jsonify({
        "gallery": gallery_data,
        "news": news_data,
        "achievement_count": achievement_count,
        "country_count": country_count,
        "user_count": user_count
    }), http.HTTP_200_OK
