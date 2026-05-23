from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

from data.models import *



# INDEX API


class Index(Resource):

    def get(self):

        return {
            "message": "Authentication API is active"
        }, 200



# REGISTER API


class RegisterAPI(Resource):

    def post(self):

        data = request.get_json()

        if not data:
            return {
                "message": "Request body is required."
            }, 400

        
        # COMMON FIELDS
        

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        
        # STUDENT FIELDS
        

        cgpa = data.get("cgpa")
        branch = data.get("branch")

        
        # COMPANY FIELDS
        

        hr_contact = data.get("hr_contact")
        website = data.get("website")

        
        # VALIDATION
        

        if not name or not email or not password or not role:
            return {
                "message": "Name, email, password and role are required."
            }, 400

        if role not in ["student", "company"]:
            return {
                "message": "Invalid role selected."
            }, 400

        
        # CHECK EXISTING USER
        

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            return {
                "message": "User already registered."
            }, 409

        
        # ROLE BASED VALIDATION
        

        if role == "student":

            if not cgpa or not branch:
                return {
                    "message": "CGPA and branch are required for students."
                }, 400

        if role == "company":

            if not hr_contact:
                return {
                    "message": "HR contact is required for company registration."
                }, 400

        
        # HASH PASSWORD
        

        hashed_password = generate_password_hash(password)

        
        # APPROVAL LOGIC
        

        approved_status = False

        # Students auto-approved
        if role == "student":
            approved_status = True

        
        # CREATE USER
        

        new_user = User(

            # Common
            name=name,
            email=email,
            password=hashed_password,
            role=role,
            approved=approved_status,

            # Student
            cgpa=cgpa if role == "student" else None,
            branch=branch if role == "student" else None,

            # Company
            hr_contact=hr_contact if role == "company" else None,
            website=website if role == "company" else None
        )

        db.session.add(new_user)
        db.session.commit()

        
        # RESPONSE MESSAGE
        

        if role == "company":

            return {
                "message": "Company registered successfully. Wait for admin approval."
            }, 201

        return {
            "message": "Student registered successfully."
        }, 201



# LOGIN API


class LoginAPI(Resource):

    def post(self):

        data = request.get_json()

        if not data:
            return {
                "message": "Invalid input."
            }, 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return {
                "message": "Email and password are required."
            }, 400

        
        # FIND USER
        

        user = User.query.filter_by(
            email=email
        ).first()

        
        # CHECK USER & PASSWORD
        

        if not user:
            return {
                "message": "User not found."
            }, 404

        if not check_password_hash(user.password, password):
            return {
                "message": "Invalid password."
            }, 401

        
        # COMPANY APPROVAL CHECK
        

        if user.role == "company" and not user.approved:

            return {
                "message": "Company account is waiting for admin approval."
            }, 403

        
        # ACCOUNT ACTIVE CHECK
        

        if hasattr(user, "is_active"):

            if user.is_active is False:

                return {
                    "message": "Your account has been deactivated by admin."
                }, 403

        
        # CREATE JWT TOKEN
        

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        
        # SUCCESS RESPONSE
        

        return {

            "message": "Login successful.",

            "access_token": access_token,

            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "approved": user.approved,

                # Student
                "cgpa": user.cgpa,
                "branch": user.branch,

                # Company
                "hr_contact": user.hr_contact,
                "website": user.website
            }

        }, 200



# PROFILE API


class ProfileAPI(Resource):

    @jwt_required()
    def get(self):

        
        # GET CURRENT USER
        

        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if not user:
            return {
                "message": "User not found."
            }, 404

        
        # RETURN PROFILE
        

        return {

            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "approved": user.approved,

            # Student Fields
            "cgpa": user.cgpa,
            "branch": user.branch,

            # Company Fields
            "hr_contact": user.hr_contact,
            "website": user.website

        }, 200