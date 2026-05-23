from flask_restful import Resource
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
    get_jwt
)

from data.models import *
from data.models import db
from datetime import datetime



# COMPANY ACCESS CHECK


def company_required():

    claims = get_jwt()

    if claims.get("role") != "company":

        return {
            "message": "Company access required."
        }, 403

    return None



# COMPANY DASHBOARD API


class CompanyDashboardAPI(Resource):

    @jwt_required()
    def get(self):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        company = User.query.get(company_id)

        total_drives = Placement.query.filter_by(
            company_id=company_id
        ).count()

        total_applications = Application.query.join(
            Placement
        ).filter(
            Placement.company_id == company_id
        ).count()

        approved_drives = Placement.query.filter_by(
            company_id=company_id,
            status="approved"
        ).count()

        pending_drives = Placement.query.filter_by(
            company_id=company_id,
            status="pending"
        ).count()

        return {

            "company": {

                "id": company.id,

                "name": company.name,

                "email": company.email,

                "website": company.website,

                "hr_contact": company.hr_contact,

                "approved": company.approved

            },

            "stats": {

                "total_drives": total_drives,

                "approved_drives": approved_drives,

                "pending_drives": pending_drives,

                "total_applications": total_applications

            }

        }, 200



# COMPANY DRIVES API


class CompanyDrivesAPI(Resource):

    @jwt_required()
    def get(self):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        drives = Placement.query.filter_by(
            company_id=company_id
        ).all()

        drive_list = []

        for drive in drives:

            applicants = Application.query.filter_by(
                drive_id=drive.id
            ).count()

            drive_list.append({

                "id": drive.id,

                "job_title": drive.job_title,

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
                    drive.status,

                "total_applicants":
                    applicants

            })

        return drive_list, 200


# CREATE PLACEMENT DRIVE


class CreateDriveAPI(Resource):

    @jwt_required()
    def post(self):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        company = User.query.get(company_id)

        if not company:

            return {
                "message": "Company not found."
            }, 404

        
        # COMPANY APPROVAL CHECK
        

        if not company.approved:

            return {
                "message": "Company not approved by admin."
            }, 403

        
        # COMPANY ACTIVE CHECK
        

        if not company.active:

            return {
                "message": "Company account is deactivated."
            }, 403

        data = request.get_json()

        if not data:

            return {
                "message": "Input data required."
            }, 400

        
        # GET DATA
        

        job_title = data.get(
            "job_title"
        )

        job_description = data.get(
            "job_description"
        )

        required_branch = data.get(
            "required_branch"
        )

        min_cgpa = data.get(
            "min_cgpa"
        )

        passing_year = data.get(
            "passing_year"
        )

        application_deadline = data.get(
            "application_deadline"
        )

        
        # VALIDATION
        

        if not all([

            job_title,
            job_description,
            required_branch,
            min_cgpa,
            passing_year,
            application_deadline

        ]):

            return {
                "message": "All fields are required."
            }, 400

        
        # DATE VALIDATION
        

        try:

            deadline_date = datetime.strptime(

                application_deadline,

                "%Y-%m-%d"

            ).date()

        except ValueError:

            return {
                "message": "Invalid date format."
            }, 400

        
        # CREATE DRIVE
        

        new_drive = Placement(

            company_id=company_id,

            job_title=job_title,

            job_description=job_description,

            required_branch=required_branch,

            min_cgpa=min_cgpa,

            passing_year=passing_year,

            application_deadline=deadline_date,

            status="pending"

        )

        db.session.add(new_drive)

        db.session.commit()

        return {

            "message":
                "Placement drive created successfully.",

            "drive": {

                "id":
                    new_drive.id,

                "job_title":
                    new_drive.job_title,

                "required_branch":
                    new_drive.required_branch,

                "min_cgpa":
                    new_drive.min_cgpa,

                "passing_year":
                    new_drive.passing_year,

                "application_deadline":
                    str(new_drive.application_deadline),

                "status":
                    new_drive.status

            }

        }, 201

# UPDATE PLACEMENT DRIVE


class UpdateDriveAPI(Resource):

    @jwt_required()
    def put(self, drive_id):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message": "Drive not found."
            }, 404

        data = request.get_json()

        if not data:

            return {
                "message": "Input data required."
            }, 400

        
        # UPDATE FIELDS
        

        drive.job_title = data.get(
            "job_title",
            drive.job_title
        )

        drive.job_description = data.get(
            "job_description",
            drive.job_description
        )

        drive.required_branch = data.get(
            "required_branch",
            drive.required_branch
        )

        drive.min_cgpa = data.get(
            "min_cgpa",
            drive.min_cgpa
        )

        drive.passing_year = data.get(
            "passing_year",
            drive.passing_year
        )

        
        # UPDATE DEADLINE
        

        application_deadline = data.get(
            "application_deadline"
        )

        if application_deadline:

            try:

                drive.application_deadline = (
                    datetime.strptime(
                        application_deadline,
                        "%Y-%m-%d"
                    ).date()
                )

            except ValueError:

                return {
                    "message": "Invalid date format."
                }, 400

        
        # RESET STATUS AFTER UPDATE
        

        drive.status = "pending"

        db.session.commit()

        return {
            "message": "Placement drive updated successfully."
        }, 200



# DELETE PLACEMENT DRIVE


class DeleteDriveAPI(Resource):

    @jwt_required()
    def delete(self, drive_id):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message": "Drive not found."
            }, 404

        db.session.delete(drive)

        db.session.commit()

        return {
            "message": "Placement drive deleted successfully."
        }, 200



# VIEW APPLICANTS


class ViewApplicantsAPI(Resource):

    @jwt_required()
    def get(self, drive_id):

        company_check = company_required()

        if company_check:
            return company_check

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message": "Drive not found."
            }, 404

        applications = Application.query.filter_by(
            drive_id=drive_id
        ).all()

        applicant_list = []

        for application in applications:

            applicant_list.append({

                "application_id":
                    application.id,

                "student_id":
                    application.student.id,

                "student_name":
                    application.student.name,

                "student_email":
                    application.student.email,

                "branch":
                    application.student.branch,

                "cgpa":
                    application.student.cgpa,

                "year":
                    application.student.year,

                "resume":
                    application.student.resume,

                "status":
                    application.status,

                "application_date":
                    str(application.application_date),

                "interview_date":
                    str(application.interview_date)
                    if application.interview_date
                    else None

            })

        return applicant_list, 200



# UPDATE APPLICATION STATUS


class UpdateApplicationStatusAPI(Resource):

    @jwt_required()
    def put(self, application_id):

        company_check = company_required()

        if company_check:
            return company_check

        data = request.get_json()

        if not data:

            return {
                "message": "Input data required."
            }, 400

        new_status = data.get("status")

        valid_status = [

            "Applied",
            "Shortlisted",
            "Selected",
            "Rejected"

        ]

        if new_status not in valid_status:

            return {
                "message": "Invalid status."
            }, 400

        application = Application.query.get(
            application_id
        )

        if not application:

            return {
                "message": "Application not found."
            }, 404

        
        # SECURITY CHECK
        

        company_id = int(get_jwt_identity())

        if application.drive.company_id != company_id:

            return {
                "message": "Unauthorized access."
            }, 403

        application.status = new_status

        db.session.commit()

        return {
            "message": "Application status updated successfully."
        }, 200



# SCHEDULE INTERVIEW API


class ScheduleInterviewAPI(Resource):

    @jwt_required()
    def put(self, application_id):

        company_check = company_required()

        if company_check:
            return company_check

        application = Application.query.get(
            application_id
        )

        if not application:

            return {
                "message": "Application not found."
            }, 404

        
        # SECURITY CHECK
        

        company_id = int(get_jwt_identity())

        if application.drive.company_id != company_id:

            return {
                "message": "Unauthorized access."
            }, 403

        data = request.get_json()

        if not data:

            return {
                "message": "Input data required."
            }, 400

        interview_date = data.get(
            "interview_date"
        )

        if not interview_date:

            return {
                "message": "Interview date required."
            }, 400

        try:

            application.interview_date = (
                datetime.strptime(
                    interview_date,
                    "%Y-%m-%d %H:%M:%S"
                )
            )

        except ValueError:

            return {
                "message": "Invalid datetime format."
            }, 400

        db.session.commit()

        return {
            "message": "Interview scheduled successfully."
        }, 200

class ShortlistedStudentsAPI(Resource):

    @jwt_required()

    def get(self):

        try:

            identity = get_jwt_identity()

            company_id = identity["id"]

            drive_id = request.args.get("drive_id")

            status = request.args.get("status")

            # ======================================
            # BASE QUERY
            # ======================================

            query = db.session.query(

                Application,
                User,
                Placement

            ).join(

                User,
                Application.student_id == User.id

            ).join(

                Placement,
                Application.drive_id == Placement.id

            ).filter(

                Placement.company_id == company_id

            ).filter(

                Application.status.in_(
                    ["Shortlisted", "Selected"]
                )

            )

            # ======================================
            # FILTER BY DRIVE
            # ======================================

            if drive_id:

                query = query.filter(
                    Placement.id == drive_id
                )

            # ======================================
            # FILTER BY STATUS
            # ======================================

            if status:

                query = query.filter(
                    Application.status == status
                )

            results = query.all()

            students = []

            for application, student, drive in results:

                students.append({

                    "application_id":
                        application.id,

                    "student_name":
                        student.name,

                    "student_email":
                        student.email,

                    "branch":
                        student.branch,

                    "cgpa":
                        student.cgpa,

                    "year":
                        student.passing_year,

                    "resume":
                        student.resume,

                    "status":
                        application.status,

                    "application_date":
                        application.applied_at,

                    "interview_date":
                        application.interview_date,

                    "job_title":
                        drive.job_title

                })

            return students, 200

        except Exception as e:

            return {

                "message":
                    "Failed to fetch shortlisted students.",

                "error":
                    str(e)

            }, 500