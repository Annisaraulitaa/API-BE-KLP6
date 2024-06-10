template = {
    "swagger": "2.0",
    # "openapi": "3.0.0",
    "info": {
        "title": "PSM API",
        "description": "API for PSM project",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "annisaraulita240702@gmail.com",
            # "url": "www.twitter.com/deve",
        },
        # "termsOfService": "www.twitter.com/deve",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}