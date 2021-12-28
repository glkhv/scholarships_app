from flask import Flask, render_template, session, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'sajdkq37432878fjjlla324fvcx'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.jinja_env.add_extension('jinja2.ext.loopcontrols')

db = SQLAlchemy(app)
db.create_all()


class Document(db.Model):
    __tablename__ = "documents"
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    title = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    event_type = db.Column(db.String(70), nullable=False)
    event_status = db.Column(db.String(70), nullable=False)
    date_of_receipt = db.Column(db.String(70), nullable=False)
    event_place = db.Column(db.String(70), nullable=False)

    def __repr__(self):
        return f"<Student {self.id}>"


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
    documents_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Application {self.id}>"


@app.route('/')
def index():

    documents = Document.query.all()
    documents_count = Document.query.count()

    applications = Application.query.filter(Application.status == 0).all()
    applications_count = Application.query.filter(
        Application.status == 0).count()

    applications_documents = get_documents(
        db.session.query(Application.documents_id).all(), Application.id)

    return render_template(
        'index.html',
        title="Уведомления",
        menu="active",
        documents=documents,
        documents_count=documents_count,
        applications=applications,
        applications_count=applications_count,
        applications_documents=applications_documents
    )


def get_documents(documents_id, id):
    array = []

    for tuples in documents_id:
        for tuple in tuples:

            list = []

            for id in tuple:
                list.append(Document.query.get(id))

            # list.append(id)

            array.append(list)

    print(array)
    return array


@app.route('/deny/<int:id>', methods=['POST'])
def deny(id):
    db.session.query(Application).filter_by(id=id).update({'status': 2})
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


@app.route('/student')
def student():
    return render_template('student.html', title="Студенты", menu="active")


@app.route('/grant')
def grant():
    return render_template('grant.html', title="Стипендии", menu="active")


# if __name__ == "__main__":
#     app.run(debug=True)
