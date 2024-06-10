import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from src.database import db
from flask_migrate import Migrate
from src.admin import admin, create_default_admin
from src.user import user
from src.structure import structure
from src.news import news
from src.achievement import achievement
from src.gallery import gallery
from src.home import home
from src.config.swagger import swagger_config, template
from src.token import token
from src.event import event
from flask_swagger_ui import get_swaggerui_blueprint # type: ignore

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            # SWAGGER={
            #     'title': "PSM API",
            #     'uiversion': 3,
            # }
        )
    else:
        app.config.from_mapping(test_config)

    # swagger config
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGER_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': 'PSM API'
        }
    )

    app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)

    JWTManager(app)

    # Initialize SQLAlchemy (db)
    db.init_app(app)

    # Initialize Flask-Migrate after db initialization
    migrate = Migrate(app, db)

    app.register_blueprint(admin, url_prefix='/api/v1/admin')
    app.register_blueprint(user, url_prefix='/api/v1/user')
    app.register_blueprint(structure, url_prefix='/api/v1/structure')
    app.register_blueprint(news, url_prefix='/api/v1/news')
    app.register_blueprint(achievement, url_prefix='/api/v1/achievements')
    app.register_blueprint(gallery, url_prefix='/api/v1/gallery')
    app.register_blueprint(home, url_prefix='/api/v1/home')
    app.register_blueprint(token, url_prefix='/api/v1/token')
    app.register_blueprint(event, url_prefix='/api/v1/event')

    Swagger(app, template=template, config=swagger_config)

    with app.app_context():
        create_default_admin()

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"msg": "Not found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({"msg": "Something went wrong"}), HTTP_500_INTERNAL_SERVER_ERROR
    
    return app
