from flask import render_template, jsonify, request, make_response
from config import app
from models import *
import io
import xlwt


@app.route('/')
def index():

    serts = Sert.query.filter(Sert.status == 2).all()
    serts_count = Sert.query.filter(Sert.status == 2).count()

    applications = Application.query.filter(Application.status == 2).all()
    applications_count = Application.query.filter(
        Application.status == 2).count()

    return render_template(
        'index.html',
        title="Уведомления",
        menu="active",
        serts=serts,
        serts_count=serts_count,
        applications=applications,
        applications_count=applications_count
    )


@app.route('/deny/<int:id>', methods=['POST'])
def deny(id):
    db.session.query(Application).filter_by(id=id).update({'status': 0})
    db.session.commit()

    resp = jsonify({"message": "Заявка отклонена"})
    resp.status_code = 200

    return resp


@app.route('/accept/<int:id>', methods=['POST'])
def accept(id):
    db.session.query(Application).filter_by(id=id).update({'status': 1})
    db.session.commit()

    resp = jsonify({"message": "Заявка принята"})
    resp.status_code = 200

    return resp


@app.route('/sert/cancel/<int:id>', methods=['POST'])
def sert_cancel(id):
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
    resp = jsonify({"message": "Документ удален"})
    resp.status_code = 200

    return resp


@app.route('/sert/accept/<int:id>', methods=['POST'])
def sert_accept(id):
    db.session.query(Sert).filter_by(id=id).update({'status': 1})
    db.session.commit()

    resp = jsonify({"message": "Документ принят"})
    resp.status_code = 200

    return resp


@app.route('/app/<int:id>', methods=['POST'])
def app_open(id):

    array = []
    app_object = {}

    application = db.session.query(Application).filter(
        Application.id == id).first()

    for i in application.documents_id:
        array.append(db.session.query(Sert).filter(Sert.id == i).first())

    app_object[0] = {
        'id': application.id,
        'fullname': application.fullname,
        'academic_group_number': application.academic_group_number,
        'type': application.type,
        'speciality_name': application.speciality_name,
        'speciality_code': application.speciality_code,
        'total_marks_count': application.total_marks_count,
        'excellent_marks_count': application.excellent_marks_count
    }

    for i, item in enumerate(array, 1):
        app_object[i] = {
            'title': item.title,
            'event_type': item.event_type,
            'event_status': item.event_status
        }

    resp = jsonify(app_object)
    resp.status_code = 200

    return resp


@app.route('/student/<int:id>', methods=['POST'])
def student_open(id):

    array = []
    students_object = {}

    students = db.session.query(Student).filter(
        Student.id == id).first()

    for i in students.documents_id:
        array.append(db.session.query(Sert).filter(Sert.id == i).first())

    students_object[0] = {
        'id': students.id,
        'fullname': students.fullname,
        'email': students.email,
        'number': students.number,
        'academic_group_number': students.academic_group_number,
        'speciality_name': students.speciality_name,
        'speciality_code': students.speciality_code
    }

    for i, item in enumerate(array, 1):
        students_object[i] = {
            'title': item.title,
            'event_type': item.event_type,
            'event_status': item.event_status
        }

    resp = jsonify(students_object)
    resp.status_code = 200

    return resp


@app.route('/students/<int:page_num>')
def student(page_num):
    students = Student.query.paginate(
        per_page=7, page=page_num, error_out=True)
    return render_template('student.html', title="Студенты", menu="active", students=students)


@app.route('/grant', methods=['GET', 'POST'])
def grant():

    applications = db.session.query(Application).filter(
        Application.status == 2).order_by(Application.id).all()

    if request.method == 'POST':
        applications_array = []
        order = request.get_data(True, True).split(',')

        print(applications, order)

        for item in order:
            applications_array.append(Application.query.get(int(item)))

        for i, app in enumerate(applications_array):
            app.order = i
            db.session.commit()

        resp = jsonify({"message": "success"})
        resp.status_code = 200

        return resp

    return render_template(
        'grant.html',
        title="Стипендии",
        menu="active",
        applications=applications
    )


@app.route('/excel', methods=['GET'])
def excel():
    applications = db.session.query(Application).filter(
        Application.status == 2).order_by(Application.order).all()

    output = io.BytesIO()
    workbook = xlwt.Workbook(encoding='utf-8')

    sh = workbook.add_sheet('Стипендии')

    sh.write(0, 0, 'Имя')
    sh.write(0, 1, '№ академической группы')
    sh.write(0, 2, 'Код')
    sh.write(0, 3, 'Специальность')
    sh.write(0, 4, 'Общее кол-во оценок')
    sh.write(0, 5, 'Кол-во оценок "Отлично"')
    sh.write(0, 6, 'Тип мероприятия')
    sh.write(0, 7, 'Статус мероприятия')
    sh.write(0, 8, 'Дата мероприятия')
    sh.write(0, 9, 'Место проведения мероприятия')

    idx = 0
    for row in applications:
        sh.write(idx+1, 0, row.fullname)
        sh.write(idx+1, 1, row.academic_group_number)
        sh.write(idx+1, 2, row.speciality_code)
        sh.write(idx+1, 3, row.speciality_name)
        sh.write(idx+1, 4, row.total_marks_count)
        sh.write(idx+1, 5, row.excellent_marks_count)

        for i, document in enumerate(row.documents_id, 1):

            doc = db.session.query(Sert).filter(Sert.id == document).first()
            print(doc, row.fullname)
            sh.write(idx+i, 6, doc.event_type)
            sh.write(idx+i, 7, doc.event_status)
            sh.write(idx+i, 8, doc.date_of_receipt)
            sh.write(idx+i, 9, doc.event_place)

        if len(row.documents_id) != 0:
            idx += len(row.documents_id)
        else:
            idx += 1

    workbook.save(output)
    output.seek(0)

    response = make_response(output.getvalue())
    # Tell the browser sent file type to Excel
    response.headers['Mime-type'] = 'application/vnd.ms-excel'
    # / saved dialog box, Data.xlsx-set file name
    response.headers['Content-Disposition'] = 'attachment; filename=data.xls'
    return response
