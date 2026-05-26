from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt
)

from sqlalchemy import or_

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
                "role": company.role,
                "approved": company.approved,
                "active": company.active,

                "company_name":
                    company.company_name,

                "industry":
                    company.industry,

                "location":
                    company.location,

                "website":
                    company.website,

                "hr_contact":
                    company.hr_contact,

                "company_description":
                    company.company_description

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
            "message":
                "Company approved successfully."
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
            "message":
                "Company rejected successfully."
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
                "message":
                    "Company already deactivated."
            }, 400

        company.active = False

        db.session.commit()

        return {
            "message":
                "Company deactivated successfully."
        }, 200


# ======================================
# ACTIVATE COMPANY
# ======================================

class ActivateCompanyAPI(Resource):

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

        if company.active:

            return {
                "message":
                    "Company already active."
            }, 400

        company.active = True

        db.session.commit()

        return {
            "message":
                "Company activated successfully."
        }, 200


# ======================================
# DELETE COMPANY
# ======================================

class DeleteCompanyAPI(Resource):

    @jwt_required()
    def delete(self, company_id):

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

        db.session.delete(company)

        db.session.commit()

        return {
            "message":
                "Company deleted successfully."
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
                "role": student.role,
                "active": student.active,

                "branch": student.branch,
                "cgpa": student.cgpa,
                "college": student.college,
                "phone": student.phone,
                "skills": student.skills,
                "year": student.year,
                "resume": student.resume

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

        student.active = False

        db.session.commit()

        return {
            "message":
                "Student deactivated successfully."
        }, 200


# ======================================
# ACTIVATE STUDENT
# ======================================

class ActivateStudentAPI(Resource):

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

        student.active = True

        db.session.commit()

        return {
            "message":
                "Student activated successfully."
        }, 200


# ======================================
# DELETE STUDENT
# ======================================

class DeleteStudentAPI(Resource):

    @jwt_required()
    def delete(self, student_id):

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

        db.session.delete(student)

        db.session.commit()

        return {
            "message":
                "Student deleted successfully."
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
                    (
                        drive.placed_company.name
                        if drive.placed_company
                        else None
                    ),

                "job_title":
                    drive.job_title,

                "job_description":
                    drive.job_description,

                "eligible_branch":
                    drive.eligible_branch,

                "min_cgpa":
                    drive.min_cgpa,

                "eligible_year":
                    drive.eligible_year,

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

        drive.status = "approved"

        db.session.commit()

        return {
            "message":
                "Placement drive approved successfully."
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

        drive.status = "rejected"

        db.session.commit()

        return {
            "message":
                "Placement drive rejected successfully."
        }, 200


# ======================================
# DELETE DRIVE
# ======================================

class DeleteDriveAPI(Resource):

    @jwt_required()
    def delete(self, drive_id):

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

        db.session.delete(drive)

        db.session.commit()

        return {
            "message":
                "Placement drive deleted successfully."
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

            job = application.job

            company_name = None
            job_title = None

            if job and job.company:
                company_name = job.company.name

            if job:
                job_title = job.title

            application_list.append({

                "application_id":
                    application.id,

                "student_id":
                    application.student.id,

                "student_name":
                    application.student.name,

                "student_email":
                    application.student.email,

                "company_name":
                    company_name,

                "job_title":
                    job_title,

                "status":
                    application.status,

                "application_date":
                    str(application.applied_at),

                "interview_date":
                    (
                        str(application.interview_date)
                        if application.interview_date
                        else None
                    )

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

            or_(

                User.name.ilike(
                    f"%{keyword}%"
                ),

                User.email.ilike(
                    f"%{keyword}%"
                ),

                User.role.ilike(
                    f"%{keyword}%"
                ),

                User.branch.ilike(
                    f"%{keyword}%"
                ),

                User.college.ilike(
                    f"%{keyword}%"
                ),

                User.skills.ilike(
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

                "active": user.active,

                "approved": user.approved

            })

        return result, 200