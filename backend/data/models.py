from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# ======================================
# DATABASE INITIALIZATION
# ======================================

db = SQLAlchemy()


# ======================================
# USER MODEL
# ======================================

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ======================================
    # BASIC INFO
    # ======================================

    name = db.Column(
        db.String(120),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # admin / company / student
    role = db.Column(
        db.String(20),
        nullable=False
    )

    approved = db.Column(
        db.Boolean,
        default=False
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ======================================
    # STUDENT PROFILE
    # ======================================

    branch = db.Column(
        db.String(100)
    )

    cgpa = db.Column(
        db.Float
    )

    year = db.Column(
        db.Integer
    )

    college = db.Column(
        db.String(150)
    )

    phone = db.Column(
        db.String(20)
    )

    skills = db.Column(
        db.Text
    )

    resume = db.Column(
        db.String(255)
    )

    # ======================================
    # COMPANY PROFILE
    # ======================================

    company_name = db.Column(
        db.String(150)
    )

    industry = db.Column(
        db.String(100)
    )

    location = db.Column(
        db.String(100)
    )

    website = db.Column(
        db.String(255)
    )

    hr_contact = db.Column(
        db.String(100)
    )

    company_description = db.Column(
        db.Text
    )

    # ======================================
    # RELATIONSHIPS
    # ======================================

    # Company -> Job Positions
    job_positions = db.relationship(
        "JobPosition",
        back_populates="company",
        lazy=True,
        foreign_keys="JobPosition.company_id"
    )

    # Student -> Applications
    applications = db.relationship(
        "Application",
        back_populates="student",
        lazy=True,
        foreign_keys="Application.student_id"
    )

    # Student -> Placements
    placements = db.relationship(
        "Placement",
        back_populates="placed_student",
        lazy=True,
        foreign_keys="Placement.student_id"
    )

    # Company -> Final Placements
    company_placements = db.relationship(
        "Placement",
        back_populates="placed_company",
        lazy=True,
        foreign_keys="Placement.company_id"
    )

    def __repr__(self):

        return f"<User {self.email}>"


# ======================================
# JOB POSITION MODEL
# ======================================

class JobPosition(db.Model):

    __tablename__ = "job_positions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    # ======================================
    # JOB DETAILS
    # ======================================

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    salary = db.Column(
        db.String(50)
    )

    skills_required = db.Column(
        db.Text
    )

    required_branch = db.Column(
        db.String(100)
    )

    min_cgpa = db.Column(
        db.Float
    )

    passing_year = db.Column(
        db.Integer
    )

    job_location = db.Column(
        db.String(100)
    )

    application_deadline = db.Column(
        db.Date
    )

    # pending / approved / rejected / closed
    status = db.Column(
        db.String(30),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ======================================
    # RELATIONSHIPS
    # ======================================

    company = db.relationship(
        "User",
        back_populates="job_positions",
        foreign_keys=[company_id]
    )

    applications = db.relationship(
        "Application",
        back_populates="job",
        lazy=True
    )

    placements = db.relationship(
        "Placement",
        back_populates="job_position",
        lazy=True
    )

    def __repr__(self):

        return f"<JobPosition {self.title}>"


# ======================================
# APPLICATION MODEL
# ======================================

class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    job_id = db.Column(
        db.Integer,
        db.ForeignKey("job_positions.id"),
        nullable=False
    )

    # Applied / Shortlisted / Selected / Rejected
    status = db.Column(
        db.String(30),
        default="Applied"
    )

    applied_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    interview_date = db.Column(
        db.DateTime
    )

    remarks = db.Column(
        db.Text
    )

    # ======================================
    # RELATIONSHIPS
    # ======================================

    student = db.relationship(
        "User",
        back_populates="applications",
        foreign_keys=[student_id]
    )

    job = db.relationship(
        "JobPosition",
        back_populates="applications",
        foreign_keys=[job_id]
    )

    def __repr__(self):

        return f"<Application {self.id}>"


# ======================================
# PLACEMENT MODEL
# ======================================

class Placement(db.Model):

    __tablename__ = "placements"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    position_id = db.Column(
        db.Integer,
        db.ForeignKey("job_positions.id"),
        nullable=False
    )

    salary = db.Column(
        db.String(50)
    )

    joining_date = db.Column(
        db.Date
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # ======================================
    # RELATIONSHIPS
    # ======================================

    placed_student = db.relationship(
        "User",
        back_populates="placements",
        foreign_keys=[student_id]
    )

    placed_company = db.relationship(
        "User",
        back_populates="company_placements",
        foreign_keys=[company_id]
    )

    job_position = db.relationship(
        "JobPosition",
        back_populates="placements",
        foreign_keys=[position_id]
    )

    def __repr__(self):

        return f"<Placement {self.id}>"