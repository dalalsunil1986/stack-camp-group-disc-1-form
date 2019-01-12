from app import app, db
from app.models import User, Form, Question, Option
from flask import request, Response, jsonify

@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']

    u = User(email=email)
    u.set_password(password)

    db.session.add(u)
    db.session.commit()

    return Response('{"data":"User created successfully."}', status=200, mimetype='application/json')

@app.route('/login', methods=['POST'])
def login():
    attempted_email = request.form['email']
    attempted_password = request.form['password']

    user = User.query.filter_by(email=attempted_email).first()
    if user is None or not user.check_password(attempted_password):
        return Response('{"data":"Invalid username or password"}', status=403, mimetype='application/json')
    return Response('{"data":"Login successfull."}', status=200, mimetype='application/json')

@app.route('/user/create-form', methods=['POST'])
def create_form():
    id_user = request.form['id_user']

    user = User.query.get(int(id_user))

    form = Form(title="Untitled", description="Default description.", creator=user)

    db.session.add(form)
    db.session.commit()

    return Response('{"data":"Form created successfully."}', status=200, mimetype='application/json')

@app.route('/user/get-all-forms', methods=['GET'])
def get_all_forms():
    id_user = request.args.get('id_user', type=int)

    forms = Form.query.filter_by(id_user=id_user)

    serialized_forms = [form.to_json() for form in forms]

    return jsonify({"data":serialized_forms})

@app.route('/user/get-one-form', methods=['GET'])
def get_one_form():
    id_form = request.args.get('id', type=int)

    form = Form.query.get(int(id_form))

    return jsonify({"data":form.to_json()})

@app.route('/user/add-question', methods=['POST'])
def add_question():
    id_form = request.form['id_form']
    label = request.form['label']
    tipe = request.form['tipe']

    question = Question(id_form=id_form, label=label, tipe=tipe)

    db.session.add(question)
    db.session.commit()

    return Response('{"data":"Question created successfully."}', status=200, mimetype='application/json')

@app.route('/user/add-option', methods=['POST'])
def add_option():
    id_question = request.form['id_question']
    label = request.form['label']    

    option = Option(id_question=id_question, label=label)

    db.session.add(option)
    db.session.commit()

    return Response('{"data":"Option created successfully."}', status=200, mimetype='application/json')

@app.route('/user/delete', methods=['POST'])
def delete():
    id = request.form['id']
    table = request.form['table']

    if table == "form":
        form = Form.query.get(int(id))
        db.session.delete(form)        
    elif table == "question":
        question = Question.query.get(int(id))
        db.session.delete(question)
    elif table == "option":
        option = Option.query.get(int(id))
        db.session.delete(option)

    db.session.commit()

    return Response('{"data":"Data deleted successfully."}', status=200, mimetype='application/json')

