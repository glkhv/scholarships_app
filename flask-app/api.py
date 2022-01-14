import os
from flask import request, jsonify
from config import app
from models import *
from base64 import b64encode
from werkzeug.utils import secure_filename
from datetime import date


@app.route('/api/application/delete/<id>', methods=['DELETE'])
def delete_application(id):
    application = Application.query.get(id)

    if(application.status == 2):
        db.session.delete(application)
        db.session.commit()

    return jsonify({"Хуйня": "Ебаная"})


@app.route('/api/application/getStatus', methods=['GET'])
def get_application_status():
    applications = Application.query.all()
    obj_array = []

    for app in applications:
        obj_array.append({"id": app.id, "status": app.status})

    return jsonify(obj_array)


@app.route('/api/sert/getStatus', methods=['GET'])
def get_sert_status():
    serts = Sert.query.all()
    obj_array = []

    for sert in serts:
        obj_array.append({"id": sert.id, "status": sert.status})

    return jsonify(obj_array)


@app.route('/api/sert/add', methods=['POST'])
def add_sert():
    status = request.json['status']
    title = request.json['title']
    name = request.json['name']
    event_type = request.json['event_type']
    event_status = request.json['event_status']
    date_of_receipt = request.json['date_of_receipt']
    event_place = request.json['event_place']
    filename = request.json['filename']

    sert = Sert(status, title, name, event_type,
                event_status, date_of_receipt, event_place, filename)
    db.session.add(sert)
    db.session.commit()

    return sert_schema.jsonify(sert)


@app.route('/api/sert/add/img', methods=['POST'])
def add_sert_img():
    img = request.files['img']

    filename = secure_filename(img.filename)
    img.save(os.path.join(
        app.config['UPLOAD_FOLDER'], filename))

    return jsonify({"Success": True})


@app.route('/api/sert/update/<id>', methods=['PUT'])
def update_sert(id):
    sert = Sert.query.get(id)

    update_obj = {}

    for key, value in request.json.items():
        update_obj[key] = value

    db.session.query(Sert).filter_by(id=id).update(update_obj)

    db.session.commit()

    return sert_schema.jsonify(sert)


@app.route('/api/application/add', methods=['POST'])
def add_application():
    status = request.json['status']
    fullname = request.json['fullname']
    type = request.json['type']
    academic_group_number = request.json['academic_group_number']
    speciality_code = request.json['speciality_code']
    speciality_name = request.json['speciality_name']
    total_marks_count = request.json['total_marks_count']
    excellent_marks_count = request.json['excellent_marks_count']
    documents_id = request.json['documents_id']
    user_id = request.json['user_id']

    application = Application(status, fullname, type, academic_group_number,
                              speciality_code, speciality_name, total_marks_count, excellent_marks_count, documents_id, user_id, 0)
    db.session.add(application)
    db.session.commit()

    return application_schema.jsonify(application)


# @app.route('/api/students/add', methods=['POST'])
# def add_student():
#     fullname = request.json['fullname']
#     email = request.json['email']
#     number = request.json['number']
#     academic_group_number = request.json['academic_group_number']
#     speciality_code = request.json['speciality_code']
#     speciality_name = request.json['speciality_name']
#     documents_id = request.json['documents_id']

#     student = Student(fullname, email, number, academic_group_number,
#                       speciality_code, speciality_name, documents_id)
#     db.session.add(student)
#     db.session.commit()

#     return student_schema.jsonify(student)


@app.route('/api/student/update', methods=['PUT'])
def update_student():
    student = Student.query.get(1)

    update_obj = {}

    for key, value in request.json.items():
        update_obj[key] = value

    db.session.query(Student).filter_by(id=1).update(update_obj)

    db.session.commit()

    return student_schema.jsonify(student)


@app.route('/api/sert/delete/<id>', methods=['DELETE'])
def delete_document(id):
    document_current = Sert.query.get(id)

    applications = Application.query.all()

    for application in applications:
        id = application.id

        documents_array = application.documents_id

        for doc in application.documents_id:
            if doc == document_current.id:
                documents_array.remove(doc)

                db.session.query(Application).filter_by(
                    id=id).update({'documents_id': documents_array})

    db.session.delete(document_current)
    db.session.commit()

    return sert_schema.jsonify(document_current)
