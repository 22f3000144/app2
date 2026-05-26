from flask_restful import Resource
from flask import request

from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)

from data.models import (
    User,
    Placement,
    Application,
    JobPosition,
    db
)

from datetime import datetime


# ======================================
# COMPANY DASHBOARD API
# ======================================

class CompanyDashboardAPI(Resource):

    @jwt_required()
    def get(self):

        company_id = int(get_jwt_identity())

        company = db.session.get(User, company_id)

        if not company:

            return {
                "message": "Company not found."
            }, 404

        # ==================================
        # DRIVE STATS
        # ==================================

        total_drives = Placement.query.filter_by(
            company_id=company_id
        ).count()

        approved_drives = Placement.query.filter_by(
            company_id=company_id,
            status="approved"
        ).count()

        pending_drives = Placement.query.filter_by(
            company_id=company_id,
            status="pending"
        ).count()

        # ==================================
        # TOTAL APPLICATIONS
        # ==================================

        total_applications = db.session.query(
            Application
        ).join(
            JobPosition,
            Application.job_id == JobPosition.id
        ).filter(
            JobPosition.company_id == company_id
        ).count()

        return {

            "company": {

                "id": company.id,
                "name": company.name,
                "email": company.email,
                "role": company.role,

                "approved": company.approved,
                "active": company.active,

                "company_name":
                    company.company_name or "",

                "industry":
                    company.industry or "",

                "location":
                    company.location or "",

                "website":
                    company.website or "",

                "hr_contact":
                    company.hr_contact or "",

                "company_description":
                    company.company_description or ""
            },

            "stats": {

                "total_drives":
                    total_drives,

                "approved_drives":
                    approved_drives,

                "pending_drives":
                    pending_drives,

                "total_applications":
                    total_applications
            }

        }, 200


# ======================================
# COMPANY DRIVES API
# ======================================

class CompanyDrivesAPI(Resource):

    @jwt_required()
    def get(self):

        company_id = int(get_jwt_identity())

        drives = Placement.query.filter_by(
            company_id=company_id
        ).all()

        drive_list = []

        for drive in drives:

            applicants = 0

            if drive.position_id:

                applicants = Application.query.filter_by(
                    job_id=drive.position_id
                ).count()

            drive_list.append({

                "id":
                    drive.id,

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
                    drive.status,

                "total_applicants":
                    applicants
            })

        return drive_list, 200


# ======================================
# CREATE PLACEMENT DRIVE
# ======================================

class CreateDriveAPI(Resource):

    @jwt_required()
    def post(self):

        company_id = int(get_jwt_identity())

        company = db.session.get(
            User,
            company_id
        )

        if not company:

            return {
                "message": "Company not found."
            }, 404

        # ==================================
        # COMPANY APPROVAL CHECK
        # ==================================

        if not company.approved:

            return {
                "message":
                    "Company not approved by admin."
            }, 403

        # ==================================
        # ACTIVE CHECK
        # ==================================

        if not company.active:

            return {
                "message":
                    "Company account is deactivated."
            }, 403

        data = request.get_json()

        if not data:

            return {
                "message":
                    "Input data required."
            }, 400

        # ==================================
        # GET DATA
        # ==================================

        job_title = data.get(
            "job_title"
        )

        job_description = data.get(
            "job_description"
        )

        eligible_branch = data.get(
            "eligible_branch"
        )

        min_cgpa = data.get(
            "min_cgpa"
        )

        eligible_year = data.get(
            "eligible_year"
        )

        application_deadline = data.get(
            "application_deadline"
        )

        location = data.get(
            "location"
        )

        salary_package = data.get(
            "salary_package"
        )

        # ==================================
        # VALIDATION
        # ==================================

        if not all([

            job_title,
            job_description,
            eligible_branch,
            eligible_year,
            application_deadline

        ]):

            return {
                "message":
                    "Required fields missing."
            }, 400

        # ==================================
        # DATE VALIDATION
        # ==================================

        try:

            deadline_date = datetime.strptime(
                application_deadline,
                "%Y-%m-%d"
            )

        except ValueError:

            return {
                "message":
                    "Invalid date format. Use YYYY-MM-DD"
            }, 400

        # ==================================
        # CREATE JOB POSITION
        # ==================================

        new_job = JobPosition(

            company_id=company_id,

            title=job_title,

            description=job_description,

            eligible_branch=eligible_branch,

            min_cgpa=float(min_cgpa),

            eligible_year=int(eligible_year),

            job_location=location,

            salary=salary_package,

            application_deadline=deadline_date.date(),

            status="pending"
        )

        db.session.add(new_job)
        db.session.flush()

        # ==================================
        # CREATE PLACEMENT DRIVE
        # ==================================

        new_drive = Placement(

            company_id=company_id,

            position_id=new_job.id,

            job_title=job_title,

            job_description=job_description,

            eligible_branch=eligible_branch,

            min_cgpa=float(min_cgpa),

            eligible_year=str(eligible_year),

            application_deadline=deadline_date,

            location=location,

            salary_package=salary_package,

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

                "eligible_branch":
                    new_drive.eligible_branch,

                "min_cgpa":
                    new_drive.min_cgpa,

                "eligible_year":
                    new_drive.eligible_year,

                "application_deadline":
                    str(new_drive.application_deadline),

                "status":
                    new_drive.status
            }

        }, 201


# ======================================
# UPDATE PLACEMENT DRIVE
# ======================================

class UpdateDriveAPI(Resource):

    @jwt_required()
    def put(self, drive_id):

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message":
                    "Drive not found."
            }, 404

        data = request.get_json()

        if not data:

            return {
                "message":
                    "Input data required."
            }, 400

        drive.job_title = data.get(
            "job_title",
            drive.job_title
        )

        drive.job_description = data.get(
            "job_description",
            drive.job_description
        )

        drive.eligible_branch = data.get(
            "eligible_branch",
            drive.eligible_branch
        )

        drive.min_cgpa = data.get(
            "min_cgpa",
            drive.min_cgpa
        )

        drive.eligible_year = data.get(
            "eligible_year",
            drive.eligible_year
        )

        drive.location = data.get(
            "location",
            drive.location
        )

        drive.salary_package = data.get(
            "salary_package",
            drive.salary_package
        )

        application_deadline = data.get(
            "application_deadline"
        )

        if application_deadline:

            try:

                drive.application_deadline = (
                    datetime.strptime(
                        application_deadline,
                        "%Y-%m-%d"
                    )
                )

            except ValueError:

                return {
                    "message":
                        "Invalid date format."
                }, 400

        drive.status = "pending"

        db.session.commit()

        return {
            "message":
                "Placement drive updated successfully."
        }, 200


# ======================================
# DELETE DRIVE
# ======================================

class DeleteDriveAPI(Resource):

    @jwt_required()
    def delete(self, drive_id):

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message":
                    "Drive not found."
            }, 404

        db.session.delete(drive)

        db.session.commit()

        return {
            "message":
                "Placement drive deleted successfully."
        }, 200


# ======================================
# VIEW APPLICANTS
# ======================================

class ViewApplicantsAPI(Resource):

    @jwt_required()
    def get(self, drive_id):

        company_id = int(get_jwt_identity())

        drive = Placement.query.filter_by(
            id=drive_id,
            company_id=company_id
        ).first()

        if not drive:

            return {
                "message":
                    "Drive not found."
            }, 404

        applications = []

        if drive.position_id:

            applications = Application.query.filter_by(
                job_id=drive.position_id
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

                "college":
                    application.student.college,

                "phone":
                    application.student.phone,

                "skills":
                    application.student.skills,

                "year":
                    application.student.year,

                "resume":
                    application.student.resume,

                "status":
                    application.status,

                "applied_at":
                    str(application.applied_at),

                "interview_date":
                    str(application.interview_date)
                    if application.interview_date
                    else None
            })

        return applicant_list, 200


# ======================================
# UPDATE APPLICATION STATUS
# ======================================

class UpdateApplicationStatusAPI(Resource):

    @jwt_required()
    def put(self, application_id):

        data = request.get_json()

        if not data:

            return {
                "message":
                    "Input data required."
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
                "message":
                    "Invalid status."
            }, 400

        application = db.session.get(
            Application,
            application_id
        )

        if not application:

            return {
                "message":
                    "Application not found."
            }, 404

        company_id = int(get_jwt_identity())

        job = db.session.get(
            JobPosition,
            application.job_id
        )

        if not job or job.company_id != company_id:

            return {
                "message":
                    "Unauthorized access."
            }, 403

        application.status = new_status

        db.session.commit()

        return {
            "message":
                "Application status updated successfully."
        }, 200


# ======================================
# SCHEDULE INTERVIEW
# ======================================

class ScheduleInterviewAPI(Resource):

    @jwt_required()
    def put(self, application_id):

        application = db.session.get(
            Application,
            application_id
        )

        if not application:

            return {
                "message":
                    "Application not found."
            }, 404

        company_id = int(get_jwt_identity())

        job = db.session.get(
            JobPosition,
            application.job_id
        )

        if not job or job.company_id != company_id:

            return {
                "message":
                    "Unauthorized access."
            }, 403

        data = request.get_json()

        if not data:

            return {
                "message":
                    "Input data required."
            }, 400

        interview_date = data.get(
            "interview_date"
        )

        if not interview_date:

            return {
                "message":
                    "Interview date required."
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
                "message":
                    "Invalid datetime format."
            }, 400

        db.session.commit()

        return {
            "message":
                "Interview scheduled successfully."
        }, 200


# ======================================
# SHORTLISTED STUDENTS API
# ======================================

class ShortlistedStudentsAPI(Resource):

    @jwt_required()
    def get(self):

        try:

            company_id = int(
                get_jwt_identity()
            )

            status = request.args.get(
                "status"
            )

            query = db.session.query(
                Application,
                User,
                JobPosition
            ).join(
                User,
                Application.student_id == User.id
            ).join(
                JobPosition,
                Application.job_id == JobPosition.id
            ).filter(
                JobPosition.company_id == company_id
            ).filter(
                Application.status.in_(
                    ["Shortlisted", "Selected"]
                )
            )

            if status:

                query = query.filter(
                    Application.status == status
                )

            results = query.all()

            students = []

            for application, student, job in results:

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

                    "college":
                        student.college,

                    "phone":
                        student.phone,

                    "skills":
                        student.skills,

                    "year":
                        student.year,

                    "resume":
                        student.resume,

                    "status":
                        application.status,

                    "applied_at":
                        str(application.applied_at),

                    "interview_date":
                        str(application.interview_date)
                        if application.interview_date
                        else None,

                    "job_title":
                        job.title
                })

            return students, 200

        except Exception as e:

            return {

                "message":
                    "Failed to fetch shortlisted students.",

                "error":
                    str(e)

            }, 500