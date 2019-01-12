from app import db
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    forms = db.relationship('Form', backref='creator', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    title = db.Column(db.String(200), index=True)
    description = db.Column(db.String(400), index=True)
    questions = db.relationship('Question', backref='form', lazy='dynamic')
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_json(self):
        return {
            "id":str(self.id),
            "timestamp":str(self.timestamp),
            "title":self.title,
            "description":self.description,
            "id_user":str(self.id_user)
        }

class QuestionType(enum.Enum):
    checkbox = "checkbox"
    radiobutton = "radiobutton"
    multiplechoice = "multiplechoice"

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), index=True)
    tipe = db.Column(db.String(100), index=True)
    id_form = db.Column(db.Integer, db.ForeignKey('form.id'))
    options = db.relationship('Option', backref='question', lazy='dynamic')

    def to_json(self):
        return {
            "id":str(self.id),
            "label":self.label,
            "tipe":self.tipe
        }

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(200), index=True)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))

    def to_json(self):
        return {
            "id":str(self.id),
            "label":self.label,
            "id_question":str(self.id_question)
        }

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    email = db.Column(db.String(200), index=True)    
    id_form = db.Column(db.Integer, db.ForeignKey('form.id'))
    answer_items = db.relationship('AnswerItem', backref='answer', lazy='dynamic')

    def to_json(self):
        return {
            "id":str(self.id),
            "timestamp":str(self.timestamp),
            "email":self.email,
            "id_form":str(self.id_form)
        }

class AnswerItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_answer = db.Column(db.Integer, db.ForeignKey('answer.id'))
    id_option = db.Column(db.Integer, db.ForeignKey('option.id'))

    def to_json(self):
        return {
            "id":str(self.id),
            "id_answer":str(self.id_answer),            
            "id_option":str(self.id_option)
        }