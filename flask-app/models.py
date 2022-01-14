from email.policy import default
from config import db, ma
from sqlalchemy.dialects import postgresql
from datetime import datetime


class Sert(db.Model):
    __tablename__ = "sertificates"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(70), nullable=False)
    event_status = db.Column(db.String(70), nullable=False)
    date_of_receipt = db.Column(db.String(70), nullable=False)
    event_place = db.Column(db.String(70), nullable=False)
    filename = db.Column(db.Text, nullable=False)

    def __init__(self, status, title, name, event_type, event_status, date_of_receipt, event_place, filename):
        self.status = status
        self.title = title
        self.name = name
        self.event_type = event_type
        self.event_status = event_status
        self.date_of_receipt = date_of_receipt
        self.event_place = event_place
        self.filename = filename

    def __repr__(self):
        return f"<Sert {self.id}>"


class SertSchema(ma.Schema):
    class Meta:
        fields = ("id", "status", "title", "name", "event_type",
                  "event_status", "date_of_receipt", "event_place", "img", "filename")


sert_schema = SertSchema()
serts_schema = SertSchema(many=True)


class Application(db.Model):
    __tablename__ = "application"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    fullname = db.Column(db.String(150), nullable=False)
    type = db.Column(db.String(150), nullable=False)
    academic_group_number = db.Column(db.String(30), nullable=False)
    speciality_code = db.Column(db.String(30), nullable=False)
    speciality_name = db.Column(db.String(100), nullable=False)
    total_marks_count = db.Column(db.Integer, nullable=False)
    excellent_marks_count = db.Column(db.Integer, nullable=False)
    documents_id = db.Column(postgresql.ARRAY(db.Integer))
    user_id = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, nullable=False)

    def __init__(self, status, fullname, type, academic_group_number, speciality_code, speciality_name, total_marks_count, excellent_marks_count, documents_id, user_id, order):
        self.status = status
        self.fullname = fullname
        self.type = type
        self.academic_group_number = academic_group_number
        self.speciality_code = speciality_code
        self.speciality_name = speciality_name
        self.total_marks_count = total_marks_count
        self.excellent_marks_count = excellent_marks_count
        self.documents_id = documents_id
        self.user_id = user_id
        self.order = order

    def __repr__(self):
        return f"<Application {self.id}>"


class ApplicationSchema(ma.Schema):
    class Meta:
        fields = ("id", "status", "fullname", "type", "academic_group_number",
                  "speciality_code", "speciality_name", "total_marks_count", "excellent_marks_count", "documents_id", "user_id", "order")


application_schema = ApplicationSchema()
applications_schema = ApplicationSchema(many=True)


class Student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    number = db.Column(db.String(150), nullable=False)
    academic_group_number = db.Column(db.String(30), nullable=False)
    speciality_code = db.Column(db.String(30), nullable=False)
    speciality_name = db.Column(db.String(100), nullable=False)
    documents_id = db.Column(postgresql.ARRAY(db.Integer))

    def __init__(self, fullname, email, number, academic_group_number, speciality_code, speciality_name, documents_id):
        self.fullname = fullname
        self.email = email
        self.number = number
        self.academic_group_number = academic_group_number
        self.speciality_code = speciality_code
        self.speciality_name = speciality_name
        self.documents_id = documents_id

    def __repr__(self):
        return f"<Student {self.id}>"


class StudentSchema(ma.Schema):
    class Meta:
        fields = ("id", "fullname", "email", "number", "academic_group_number",
                  "speciality_code", "speciality_name", "documents_id")


student_schema = StudentSchema()
students_schema = StudentSchema(many=True)
