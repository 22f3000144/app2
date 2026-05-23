from backend.controllers.company_api import ShortlistedStudentsAPI
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

    from controllers.admin_api import (

        # ======================================
        # ADMIN APIs
        # ======================================

        AdminDashboardAPI,
        ManageCompaniesAPI,
        ApproveCompanyAPI,
        RejectCompanyAPI,
        DeactivateCompanyAPI,
        # ReportsAPI,
        ManageStudentsAPI,
        DeactivateStudentAPI,

        ManageDrivesAPI,
        ApproveDriveAPI,
        RejectDriveAPI,

        ViewApplicationsAPI,
        SearchUsersAPI,
    )
        # ======================================
        # COMPANY APIs 
        # ======================================
    from controllers.company_api import (
        CompanyDashboardAPI,
        CreateDriveAPI,
        CompanyDrivesAPI,
        UpdateDriveAPI,
        DeleteDriveAPI,
        ShortlistedStudentsAPI,
        ViewApplicantsAPI,
        UpdateApplicationStatusAPI,
        ScheduleInterviewAPI
    )


    # ======================================
    # BASIC ROUTES
    # ======================================

    app.add_url_rule(
        "/",
        view_func=lambda: {
            "message": "Eduvora Backend Running"
        }
    )


    # ======================================
    # HEALTH CHECK
    # ======================================

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


    # ======================================
    # ADMIN ROUTES
    # ======================================

    api.add_resource(
        AdminDashboardAPI,
        "/api/admin/dashboard"
    )

    api.add_resource(
        ManageCompaniesAPI,
        "/api/admin/companies"
    )

    api.add_resource(
        ApproveCompanyAPI,
        "/api/admin/company/approve/<int:company_id>"
    )

    api.add_resource(
        RejectCompanyAPI,
        "/api/admin/company/reject/<int:company_id>"
    )

    api.add_resource(
        DeactivateCompanyAPI,
        "/api/admin/company/deactivate/<int:company_id>"
    )

    api.add_resource(
        ManageStudentsAPI,
        "/api/admin/students"
    )

    api.add_resource(
        DeactivateStudentAPI,
        "/api/admin/student/deactivate/<int:student_id>"
    )

    api.add_resource(
        ManageDrivesAPI,
        "/api/admin/drives"
    )

    api.add_resource(
        ApproveDriveAPI,
        "/api/admin/drive/approve/<int:drive_id>"
    )

    api.add_resource(
        RejectDriveAPI,
        "/api/admin/drive/reject/<int:drive_id>"
    )

    api.add_resource(
        ViewApplicationsAPI,
        "/api/admin/applications"
    )

    api.add_resource(
        SearchUsersAPI,
        "/api/admin/search"
    )


    # ======================================
    # COMPANY ROUTES
    # ======================================

    api.add_resource(
        CompanyDashboardAPI,
        "/api/company/dashboard"
    )

    api.add_resource(
        CreateDriveAPI,
        "/api/company/drive/create"
    )
    api.add_resource(
        ShortlistedStudentsAPI,
        "/api/company/shortlisted-students"
    )
    api.add_resource(
        CompanyDrivesAPI,
        "/api/company/drives"
    )

    api.add_resource(
        UpdateDriveAPI,
        "/api/company/drive/update/<int:drive_id>"
    )

    api.add_resource(
        DeleteDriveAPI,
        "/api/company/drive/delete/<int:drive_id>"
    )

    api.add_resource(
        ViewApplicantsAPI,
        "/api/company/applicants/<int:drive_id>"
    )

    api.add_resource(
        UpdateApplicationStatusAPI,
        "/api/company/application/status/<int:application_id>"
    )

    api.add_resource(
        ScheduleInterviewAPI,
        "/api/company/interview/schedule/<int:application_id>"
    )


    return app, celery

app, celery = create_app()

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )