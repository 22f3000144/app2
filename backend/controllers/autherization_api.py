from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from data.models import *


# ======================================
# INDEX
# ======================================

class Index(Resource):
    def get(self):
        return {"message": "Authentication API is active"}, 200


# ======================================
# REGISTER API
# ======================================

class RegisterAPI(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "Credentials required."}, 400

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")  # student / company

        cgpa = data.get("cgpa")
        branch = data.get("branch")

        # Basic validation
        if not name or not email or not password or not role:
            return {"message": "All required fields must be provided."}, 400

        if role not in ["student", "company"]:
            return {"message": "Invalid role selected."}, 400

        # Check existing user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already registered."}, 409

        # Hash password
        hashed_password = generate_password_hash(password)

        # Company approval logic
        approved_status = False
        if role == "student":
            approved_status = True  # students auto-approved

        # Create new user
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            approved=approved_status,
            cgpa=cgpa if role == "student" else None,
            branch=branch if role == "student" else None
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User registered successfully."}, 201


# ======================================
# LOGIN API
# ======================================

class LoginAPI(Resource):
    def post(self):
        data = request.get_json()

        if not data:
            return {"message": "Invalid input."}, 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {"message": "Email and password required."}, 400

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {"message": "Invalid credentials."}, 401

        # Company must be approved before login
        if user.role == "company" and not user.approved:
            return {"message": "Company not approved by admin yet."}, 403

        # Create JWT token
        access_token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role}
        )

        return {
            "message": "Login successful.",
            "access_token": access_token,
            "role": user.role,
            "name": user.name,
            "email": user.email
        }, 200


# ======================================
# PROFILE API
# ======================================

class ProfileAPI(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "approved": user.approved,
            "cgpa": user.cgpa,
            "branch": user.branch
        }, 200