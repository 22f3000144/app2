from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from data.models import *


# =========================================
# INDEX API
# =========================================

class Index(Resource):

    def get(self):

        return {
            "message": "Authentication API is active"
        }, 200


# =========================================
# REGISTER API
# =========================================

class RegisterAPI(Resource):

    def post(self):

        data = request.get_json()

        if not data:

            return {
                "message": "Request body is required."
            }, 400

        # =========================================
        # COMMON FIELDS
        # =========================================

        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        # =========================================
        # STUDENT FIELDS
        # =========================================

        cgpa = data.get("cgpa")
        branch = data.get("branch")
        year = data.get("year")

        college = data.get("college")
        phone = data.get("phone")

        skills = data.get("skills")
        resume = data.get("resume")

        # =========================================
        # COMPANY FIELDS
        # =========================================

        company_name = data.get("company_name")
        industry = data.get("industry")
        location = data.get("location")

        hr_contact = data.get("hr_contact")
        website = data.get("website")

        company_description = data.get(
            "company_description"
        )

        # =========================================
        # VALIDATION
        # =========================================

        if not name or not email or not password or not role:

            return {
                "message": (
                    "Name, email, password "
                    "and role are required."
                )
            }, 400

        # =========================================
        # ROLE CHECK
        # =========================================

        if role not in ["student", "company"]:

            return {
                "message": "Invalid role selected."
            }, 400

        # =========================================
        # CHECK EXISTING USER
        # =========================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

            return {
                "message": "User already registered."
            }, 409

        # =========================================
        # STUDENT VALIDATION
        # =========================================

        if role == "student":

            if cgpa is None or not branch:

                return {
                    "message": (
                        "CGPA and branch are "
                        "required for students."
                    )
                }, 400

        # =========================================
        # COMPANY VALIDATION
        # =========================================

        if role == "company":

            if not hr_contact:

                return {
                    "message": (
                        "HR contact is required "
                        "for company registration."
                    )
                }, 400

        # =========================================
        # HASH PASSWORD
        # =========================================

        hashed_password = generate_password_hash(
            password
        )

        # =========================================
        # APPROVAL LOGIC
        # =========================================

        approved_status = False

        # Students auto approved
        if role == "student":

            approved_status = True

        # =========================================
        # CREATE USER
        # =========================================

        new_user = User(

            # =====================================
            # COMMON
            # =====================================

            name=name,
            email=email,
            password=hashed_password,
            role=role,

            approved=approved_status,

            # =====================================
            # STUDENT
            # =====================================

            cgpa=(
                cgpa
                if role == "student"
                else None
            ),

            branch=(
                branch
                if role == "student"
                else None
            ),

            year=(
                year
                if role == "student"
                else None
            ),

            college=(
                college
                if role == "student"
                else None
            ),

            phone=(
                phone
                if role == "student"
                else None
            ),

            skills=(
                skills
                if role == "student"
                else None
            ),

            resume=(
                resume
                if role == "student"
                else None
            ),

            # =====================================
            # COMPANY
            # =====================================

            company_name=(
                company_name
                if role == "company"
                else None
            ),

            industry=(
                industry
                if role == "company"
                else None
            ),

            location=(
                location
                if role == "company"
                else None
            ),

            hr_contact=(
                hr_contact
                if role == "company"
                else None
            ),

            website=(
                website
                if role == "company"
                else None
            ),

            company_description=(
                company_description
                if role == "company"
                else None
            )
        )

        db.session.add(new_user)

        db.session.commit()

        # =========================================
        # RESPONSE
        # =========================================

        if role == "company":

            return {
                "message": (
                    "Company registered successfully. "
                    "Wait for admin approval."
                )
            }, 201

        return {
            "message": (
                "Student registered successfully."
            )
        }, 201


# =========================================
# LOGIN API
# =========================================

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
                "message": (
                    "Email and password "
                    "are required."
                )
            }, 400

        # =========================================
        # FIND USER
        # =========================================

        user = User.query.filter_by(
            email=email
        ).first()

        if not user:

            return {
                "message": "User not found."
            }, 404

        # =========================================
        # PASSWORD CHECK
        # =========================================

        if not check_password_hash(
            user.password,
            password
        ):

            return {
                "message": "Invalid password."
            }, 401

        # =========================================
        # COMPANY APPROVAL CHECK
        # =========================================

        if (
            user.role == "company"
            and not user.approved
        ):

            return {
                "message": (
                    "Company account is waiting "
                    "for admin approval."
                )
            }, 403

        # =========================================
        # ACTIVE CHECK
        # =========================================

        if hasattr(user, "active"):

            if user.active is False:

                return {
                    "message": (
                        "Your account has been "
                        "deactivated by admin."
                    )
                }, 403

        # =========================================
        # CREATE JWT TOKEN
        # =========================================

        access_token = create_access_token(

            identity=str(user.id),

            additional_claims={
                "role": user.role
            }
        )

        # =========================================
        # SUCCESS RESPONSE
        # =========================================

        return {

            "message": "Login successful.",

            "access_token": access_token,

            "user": {

                # =================================
                # COMMON
                # =================================

                "id": user.id,
                "name": user.name,
                "email": user.email,

                "role": user.role,

                "approved": user.approved,

                "active": user.active,

                # =================================
                # STUDENT
                # =================================

                "cgpa": user.cgpa,
                "branch": user.branch,
                "year": user.year,

                "college": user.college,
                "phone": user.phone,

                "skills": user.skills,
                "resume": user.resume,

                # =================================
                # COMPANY
                # =================================

                "company_name": user.company_name,
                "industry": user.industry,
                "location": user.location,

                "hr_contact": user.hr_contact,
                "website": user.website,

                "company_description":
                    user.company_description
            }

        }, 200


# =========================================
# PROFILE API
# =========================================

class ProfileAPI(Resource):

    @jwt_required()
    def get(self):

        # =========================================
        # GET CURRENT USER
        # =========================================

        user_id = int(
            get_jwt_identity()
        )

        user = User.query.get(user_id)

        if not user:

            return {
                "message": "User not found."
            }, 404

        # =========================================
        # RETURN PROFILE
        # =========================================

        return {

            # =====================================
            # COMMON
            # =====================================

            "id": user.id,
            "name": user.name,
            "email": user.email,

            "role": user.role,

            "approved": user.approved,

            "active": user.active,

            # =====================================
            # STUDENT
            # =====================================

            "cgpa": user.cgpa,
            "branch": user.branch,
            "year": user.year,

            "college": user.college,
            "phone": user.phone,

            "skills": user.skills,
            "resume": user.resume,

            # =====================================
            # COMPANY
            # =====================================

            "company_name": user.company_name,
            "industry": user.industry,
            "location": user.location,

            "hr_contact": user.hr_contact,
            "website": user.website,

            "company_description":
                user.company_description

        }, 200
    @jwt_required()
    def put(self):

        user_id = int(get_jwt_identity())

        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found."}, 404

        data = request.get_json()

        if not data:
            return {"message": "Input data required."}, 400

        # ======================================
        # COMMON FIELDS
        # ======================================

        user.name = data.get("name", user.name)

        # NOTE: email update optional (enable only if allowed in your system)
        user.email = data.get("email", user.email)

        # ======================================
        # STUDENT FIELDS
        # ======================================

        user.cgpa = data.get("cgpa", user.cgpa)
        user.branch = data.get("branch", user.branch)
        user.year = data.get("year", user.year)
        user.college = data.get("college", user.college)
        user.phone = data.get("phone", user.phone)
        user.skills = data.get("skills", user.skills)
        user.resume = data.get("resume", user.resume)

        # ======================================
        # COMPANY FIELDS
        # ======================================

        user.company_name = data.get("company_name", user.company_name)
        user.industry = data.get("industry", user.industry)
        user.location = data.get("location", user.location)
        user.hr_contact = data.get("hr_contact", user.hr_contact)
        user.website = data.get("website", user.website)
        user.company_description = data.get(
            "company_description",
            user.company_description
        )

        # ======================================
        # SAVE
        # ======================================

        db.session.commit()

        return {
            "message": "Profile updated successfully."
        }, 200