from app import app, db
from app.models import User, Form, Question, Option, Answer, AnswerItem
from flask import request, Response, jsonify
import json

@app.route('/guest/fill-form', methods=['GET'])
def fill_form():
    id_form = request.args.get('id_form', type=int)

    form = Form.query.get(int(id_form))
    questions = Question.query.filter_by(id_form=id_form)

    serialized_questions = []

    for question in questions:

        question_json = question.to_json()

        options = Option.query.filter_by(id_question=question.id)

        question_json["options"] = [option.to_json() for option in options]

        serialized_questions.append(question_json)
    
    form_json = form.to_json()

    form_json["questions"] = serialized_questions

    return jsonify({"data":form_json})

@app.route('/guest/create-answer', methods=['POST'])
def create_answer():
    id_form = request.form["id_form"]
    email = request.form["email"]
    selected_options = json.loads(request.form["selected_options"])

    answer = Answer(email=email, id_form=id_form)

    db.session.add(answer)
    db.session.commit()

    for option_id in selected_options:
        answerItem = AnswerItem(id_answer=answer.id, id_option=option_id)
        db.session.add(answerItem)
        db.session.commit()
    
    return Response('{"data":"Answer submited successfully."}', status=200, mimetype='application/json')


