from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail
from flask_cors import CORS
from celery import Celery
from datetime import timedelta

from data.models import db
from data.models import *

from controllers.config import LocalDevelopmentConfig

from werkzeug.security import generate_password_hash


# ======================================
# GLOBAL EXTENSIONS
# ======================================

cache = Cache()
mail = Mail()


# ======================================
# CELERY INITIALIZATION
# ======================================

def init_celery(flask_app):

    celery_app = Celery(
        flask_app.import_name,
        broker=flask_app.config["CELERY_BROKER_URL"],
        backend=flask_app.config["CELERY_RESULT_BACKEND"]
    )

    celery_app.conf.update(flask_app.config)

    class ContextTask(celery_app.Task):

        def __call__(self, *args, **kwargs):

            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery_app.Task = ContextTask

    return celery_app


# ======================================
# CREATE DEFAULT ADMIN
# ======================================

def create_admin():

    admin = User.query.filter_by(
        email="admin@gmail.com"
    ).first()

    if not admin:

        admin = User(
            name="Admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin123"),
            role="admin",
            approved=True,
            active=True
        )

        db.session.add(admin)
        db.session.commit()
# ======================================
# APPLICATION FACTORY
# ======================================

def create_app():

    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    app.config["SECRET_KEY"] = "placement-secret-key"
    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    db.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)
    cache.init_app(app)
    mail.init_app(app)

    CORS(
        app,
        resources={
            r"/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://127.0.0.1:5173"
                ],
                "supports_credentials": True
            }
        }
    )

    # ======================================
    # INITIALIZE CELERY
    # ======================================

    celery = init_celery(app)

    with app.app_context():
        db.create_all()
        create_admin()

    from controllers.autherization_api import (
        Index,
        RegisterAPI,
        LoginAPI,
        ProfileAPI
    )

    # Basic Route
    app.add_url_rule(
        "/",
        view_func=lambda: {
            "message": "Eduvora Backend Running"
        }
    )

    # Health Check
    @app.route("/check")
    def check():

        return {
            "status": "success",
            "message": "Eduvora Backend Running"
        }, 200

    # ======================================
    # AUTH ROUTES
    # ======================================

    api.add_resource(
        Index,
        "/api"
    )

    api.add_resource(
        RegisterAPI,
        "/api/register"
    )

    api.add_resource(
        LoginAPI,
        "/api/login"
    )

    api.add_resource(
        ProfileAPI,
        "/api/profile"
    )

    return app, celery

app, celery = create_app()

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )