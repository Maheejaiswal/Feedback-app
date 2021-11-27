from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:2906@localhost/feedback'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://dxmvghwqfvtrsr:213006348281db817e2b66164bf8474c8234c3a4159ac7e3dc4fd9de5780d896@ec2-54-208-96-16.compute-1.amazonaws.com:5432/den4tsc6kdko6f'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    student = db.Column(db.String(200), unique=True)
    teacher = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, student, teacher, rating, comments):
        self.student = student
        self.teacher = teacher
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        student = request.form['student']
        teacher = request.form['teacher']
        rating = request.form['rating']
        comments = request.form['comments']
        if student == '' or teacher == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.student == student).count() == 0:
            data = Feedback(student, teacher, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(student, teacher, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')


if __name__ == '__main__':
    app.run()