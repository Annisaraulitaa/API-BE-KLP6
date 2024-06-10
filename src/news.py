from datetime import datetime
import uuid

from flask_jwt_extended import get_jwt_identity, jwt_required
import src.constants.http_status_codes as http
from flask import Blueprint, jsonify, request
from src.database import News, db
from src.utils.upload_image_to_firebase import upload_image_to_firebase

news = Blueprint('news', __name__)

@news.get('/')
def get_news():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = News.query.paginate(page, per_page, False)
    news_items = pagination.items
    
    return jsonify({
        "data": [n.to_dict() for n in news_items],
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages
    }), http.HTTP_200_OK

@news.get('/<news_id>')
def get_news_by_id(news_id):
    news: News = News.query.filter_by(id=news_id).first()
    
    if news:
        return jsonify({
            "data": news.to_dict()
        }), http.HTTP_200_OK
    
    return jsonify({"msg": "News not found"}), http.HTTP_404_NOT_FOUND

@news.post('/create')
@jwt_required()
def create_news():
    created_by = get_jwt_identity()
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    photo = request.form.get('photo', None)
    
    if not title or not content or not photo:
        return jsonify({"msg": "Title, content, and photo are required"}), http.HTTP_400_BAD_REQUEST
    
    new_id = str(uuid.uuid4())
    photo_url = upload_image_to_firebase(photo, file_name=f'news/{new_id}')
    if not photo_url[0]:
        return jsonify({
            'msg': photo_url[1]
        }), http.HTTP_500_INTERNAL_SERVER_ERROR
    
    created_at = datetime.now().timestamp() * 1000

    news = News(
        id=new_id,
        title=title,
        content=content,
        photo_url=photo_url[0],
        updated_at=created_at,
        created_at=created_at,
        created_by=created_by,
    )
    
    db.session.add(news)
    db.session.commit()
    
    return jsonify({
        "msg": "News created successfully",
        "data": news.to_dict()
    }), http.HTTP_201_CREATED

@news.put('/update/<news_id>')
@jwt_required()
def update_news(news_id):
    title = request.form.get('title', None)
    content = request.form.get('content', None)
    photo = request.form.get('photo', None)
    
    news: News = News.query.get(news_id)
    
    if news:
        if photo:
            # save image to firebase storage
            photo_url = upload_image_to_firebase(photo, file_name=f'news/{news_id}')
            if not photo_url[0]:
                return jsonify({
                    'msg': photo_url[1]
                }), http.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                news.photo_url = photo_url[0]
        
        if title: news.title = title
        if content: news.content = content
        news.updated_at = datetime.now().timestamp() * 1000
        
        db.session.commit()
        
        return jsonify({
            "msg": "News updated successfully",
            "data": news.to_dict()
        }), http.HTTP_200_OK
    
    return jsonify({"msg": "News not found"}), http.HTTP_404_NOT_FOUND

@news.delete('/delete/<news_id>')
@jwt_required()
def delete_news(news_id):
    news: News = News.query.get(news_id)
    
    if news:
        db.session.delete(news)
        db.session.commit()
        
        return jsonify({
            "msg": "News deleted successfully",
            "data": news.to_dict()
        }), http.HTTP_200_OK
    
    return jsonify({"msg": "News not found"}), http.HTTP_404_NOT_FOUND