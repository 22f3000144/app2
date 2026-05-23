from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from data.models import (
    db,
    User,
    Placement,
    Application
)


# ======================================
# ADMIN ACCESS CHECK
# ======================================

def admin_required():

    claims = get_jwt()

    if claims.get("role") != "admin":

        return {
            "message": "Admin access required."
        }, 403

    return None


# ======================================
# ADMIN DASHBOARD API
# ======================================

class AdminDashboardAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        total_students = User.query.filter_by(
            role="student",
            active=True
        ).count()

        total_companies = User.query.filter_by(
            role="company",
            active=True
        ).count()

        total_drives = Placement.query.count()

        total_applications = Application.query.count()

        approved_companies = User.query.filter_by(
            role="company",
            approved=True
        ).count()

        pending_companies = User.query.filter_by(
            role="company",
            approved=False
        ).count()

        return {

            "total_students": total_students,

            "total_companies": total_companies,

            "approved_companies":
                approved_companies,

            "pending_companies":
                pending_companies,

            "total_drives": total_drives,

            "total_applications":
                total_applications

        }, 200


# ======================================
# GET ALL COMPANIES
# ======================================

class ManageCompaniesAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        companies = User.query.filter_by(
            role="company"
        ).all()

        company_list = []

        for company in companies:

            company_list.append({

                "id": company.id,

                "name": company.name,

                "email": company.email,

                "website": company.website,

                "hr_contact": company.hr_contact,

                "approved": company.approved,

                "active": company.active

            })

        return company_list, 200


# ======================================
# APPROVE COMPANY
# ======================================

class ApproveCompanyAPI(Resource):

    @jwt_required()
    def put(self, company_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        company = User.query.filter_by(
            id=company_id,
            role="company"
        ).first()

        if not company:

            return {
                "message": "Company not found."
            }, 404

        if company.approved:

            return {
                "message": "Company already approved."
            }, 400

        company.approved = True

        db.session.commit()

        return {
            "message": "Company approved successfully."
        }, 200


# ======================================
# REJECT COMPANY
# ======================================

class RejectCompanyAPI(Resource):

    @jwt_required()
    def put(self, company_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        company = User.query.filter_by(
            id=company_id,
            role="company"
        ).first()

        if not company:

            return {
                "message": "Company not found."
            }, 404

        company.approved = False

        db.session.commit()

        return {
            "message": "Company rejected successfully."
        }, 200


# ======================================
# DEACTIVATE COMPANY
# ======================================

class DeactivateCompanyAPI(Resource):

    @jwt_required()
    def put(self, company_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        company = User.query.filter_by(
            id=company_id,
            role="company"
        ).first()

        if not company:

            return {
                "message": "Company not found."
            }, 404

        if not company.active:

            return {
                "message": "Company already deactivated."
            }, 400

        company.active = False

        db.session.commit()

        return {
            "message": "Company deactivated successfully."
        }, 200


# ======================================
# GET ALL STUDENTS
# ======================================

class ManageStudentsAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        students = User.query.filter_by(
            role="student"
        ).all()

        student_list = []

        for student in students:

            student_list.append({

                "id": student.id,

                "name": student.name,

                "email": student.email,

                "branch": student.branch,

                "cgpa": student.cgpa,

                "year": student.year,

                "resume": student.resume,

                "active": student.active

            })

        return student_list, 200


# ======================================
# DEACTIVATE STUDENT
# ======================================

class DeactivateStudentAPI(Resource):

    @jwt_required()
    def put(self, student_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        student = User.query.filter_by(
            id=student_id,
            role="student"
        ).first()

        if not student:

            return {
                "message": "Student not found."
            }, 404

        if not student.active:

            return {
                "message": "Student already deactivated."
            }, 400

        student.active = False

        db.session.commit()

        return {
            "message": "Student deactivated successfully."
        }, 200


# ======================================
# GET ALL PLACEMENT DRIVES
# ======================================

class ManageDrivesAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        drives = Placement.query.all()

        drive_list = []

        for drive in drives:

            drive_list.append({

                "id": drive.id,

                "company_id":
                    drive.company_id,

                "company_name":
                    drive.company.name,

                "job_title":
                    drive.job_title,

                "job_description":
                    drive.job_description,

                "required_branch":
                    drive.required_branch,

                "min_cgpa":
                    drive.min_cgpa,

                "passing_year":
                    drive.passing_year,

                "application_deadline":
                    str(drive.application_deadline),

                "status":
                    drive.status

            })

        return drive_list, 200


# ======================================
# APPROVE DRIVE
# ======================================

class ApproveDriveAPI(Resource):

    @jwt_required()
    def put(self, drive_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        drive = db.session.get(
            Placement,
            drive_id
        )

        if not drive:

            return {
                "message": "Drive not found."
            }, 404

        if drive.status == "approved":

            return {
                "message": "Drive already approved."
            }, 400

        drive.status = "approved"

        db.session.commit()

        return {
            "message": "Placement drive approved successfully."
        }, 200


# ======================================
# REJECT DRIVE
# ======================================

class RejectDriveAPI(Resource):

    @jwt_required()
    def put(self, drive_id):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        drive = db.session.get(
            Placement,
            drive_id
        )

        if not drive:

            return {
                "message": "Drive not found."
            }, 404

        if drive.status == "rejected":

            return {
                "message": "Drive already rejected."
            }, 400

        drive.status = "rejected"

        db.session.commit()

        return {
            "message": "Placement drive rejected successfully."
        }, 200


# ======================================
# VIEW ALL APPLICATIONS
# ======================================

class ViewApplicationsAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        applications = Application.query.all()

        application_list = []

        for application in applications:

            application_list.append({

                "application_id":
                    application.id,

                "student_name":
                    application.student.name,

                "student_email":
                    application.student.email,

                "company_name":
                    application.drive.company.name,

                "job_title":
                    application.drive.job_title,

                "status":
                    application.status,

                "application_date":
                    str(application.application_date),

                "interview_date":
                    str(application.interview_date)
                    if application.interview_date
                    else None

            })

        return application_list, 200


# ======================================
# SEARCH USERS API
# ======================================

class SearchUsersAPI(Resource):

    @jwt_required()
    def get(self):

        admin_check = admin_required()

        if admin_check:
            return admin_check

        keyword = request.args.get(
            "keyword",
            ""
        ).strip()

        if not keyword:

            return {
                "message": "Keyword required."
            }, 400

        users = User.query.filter(

            db.or_(

                User.name.ilike(
                    f"%{keyword}%"
                ),

                User.email.ilike(
                    f"%{keyword}%"
                ),

                User.role.ilike(
                    f"%{keyword}%"
                )

            )

        ).all()

        result = []

        for user in users:

            result.append({

                "id": user.id,

                "name": user.name,

                "email": user.email,

                "role": user.role,

                "active": user.active

            })

        return result, 200