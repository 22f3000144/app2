from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


# ======================================
# USER MODEL
# ======================================
 
class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # admin / student / company
    role = db.Column(db.String(20), nullable=False)
    approved = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    # Student fields
    cgpa = db.Column(db.Float)
    branch = db.Column(db.String(100))
    year = db.Column(db.Integer)
    resume = db.Column(db.String(255))
    # Company fields
    company_name = db.Column(db.String(150))
    website = db.Column(db.String(255))
    hr_contact = db.Column(db.String(100))
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    # Relationships
    drives = db.relationship(
        "PlacementDrive",
        backref="company",
        lazy=True
    )

    applications = db.relationship(
        "Application",
        backref="student",
        lazy=True
    )

    def __repr__(self):
        return f"<User {self.email}>"



# ======================================
# PLACEMENT DRIVE MODEL
# ======================================

class PlacementDrive(db.Model):

    __tablename__ = "placement_drives"

    id = db.Column(db.Integer, primary_key=True)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    job_title = db.Column(
        db.String(150),
        nullable=False
    )

    job_description = db.Column(
        db.Text,
        nullable=False
    )

    required_branch = db.Column(
        db.String(100),
        nullable=False
    )

    min_cgpa = db.Column(
        db.Float,
        nullable=False
    )

    passing_year = db.Column(
        db.Integer,
        nullable=False
    )

    application_deadline = db.Column(
        db.Date,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relationships
    applications = db.relationship(
        "Application",
        backref="drive",
        lazy=True
    )

    def __repr__(self):
        return f"<Drive {self.job_title}>"



# ======================================
# APPLICATION MODEL
# ======================================

class Application(db.Model):

    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("placement_drives.id"),
        nullable=False
    )

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

    def __repr__(self):
        return f"<Application {self.id}>"