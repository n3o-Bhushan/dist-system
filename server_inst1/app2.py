from flask import Flask, jsonify, request, Response, json, Request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import redis


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bhushan@localhost/expenseManagement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db1 = SQLAlchemy(app)
DATABASE = 'expenseManagement'


class Expense_register(db1.Model):
    __tablename__ = 'expense_register'
    expense_id = db1.Column(db1.Integer, primary_key=True, nullable=False)
    name = db1.Column(db1.Unicode(20), nullable=False)
    email = db1.Column(db1.Unicode(40), nullable=False)
    category = db1.Column(db1.Unicode(90), nullable=False)
    description = db1.Column(db1.Unicode(50), nullable=False)
    link = db1.Column(db1.Unicode(60), nullable=False)
    estimated_costs = db1.Column(db1.Unicode(10), nullable=False)
    submit_date = db1.Column(db1.Unicode(10), nullable=False)
    status = db1.Column(db1.Unicode(15), nullable=False)
    decision_date = db1.Column(db1.Unicode(10), nullable=False)

    def __init__(self, name, email, category, description, link, status, estimated_costs, submit_date, decision_date):
        # self.expense_id=expense_id
        self.category = category
        self.description = description
        self.name = name
        self.email = email
        self.link = link
        self.status = status
        self.decision_date = decision_date
        self.estimated_costs = estimated_costs
        self.submit_date = submit_date


@app.route('/v1/expenses', methods=['POST'])
def postExpense():
    expense = request.get_json(force='True')
    # expense_id=expense["id"]
    name = expense["name"]
    email = expense['email']
    category = expense['category']
    description = expense['description']
    link = expense['link']
    submit_date = expense['submit_date']
    estimated_costs = expense['estimated_costs']
    status = 'pending'
    decision_date = ''

    engine = create_engine("mysql://root:bhushan@localhost")
    engine.execute("CREATE DATABASE IF NOT EXISTS %s " % (DATABASE))
    engine.execute("USE %s " % (DATABASE))
    db1.create_all()
    first_new = Expense_register(name, email, category, description, link, status, estimated_costs, submit_date,
                                 decision_date)
    db1.session.add(first_new)
    db1.session.commit()

    data = {'id': str(first_new.expense_id), 'name': name, 'email': email, 'category': category,
            'description': description, 'link': link, 'estimated_costs': estimated_costs, 'submit_date': submit_date,
            'status': status, 'decision_date': decision_date}
    resp = Response(response=json.dumps(data),
                    status=201,
                    mimetype="application/json")
    return resp


@app.route('/v1/expenses/<string:expense_id>', methods=['GET'])
def returnOne(expense_id):
    expense = Expense_register.query.filter_by(expense_id=expense_id).first()
    if expense == None:
        resp = Response(response=None, status=404, mimetype="application/json")
        return resp
    data = {'id': str(expense.expense_id), 'name': expense.name, 'email': expense.email, 'category': expense.category,
            'description': expense.description, 'link': expense.link, 'estimated_costs': expense.estimated_costs,
            'submit_date': expense.submit_date, 'status': expense.status, 'decision_date': expense.decision_date}
    resp = Response(response=json.dumps(data), status=200, mimetype="application/json")
    return resp


@app.route('/v1/expenses/<string:expense_id>', methods=['PUT'])
def updateExpense(expense_id):
    expense = request.get_json(force='True')
    update = Expense_register.query.filter_by(expense_id=expense_id).first()

    for i in expense:

        if (i == 'estimated_costs'):
            update.estimated_costs = expense[i]
        elif (i == 'category'):
            update.category = expense[i]
        elif (i == 'name'):
            update.name = expense[i]
        elif (i == 'email'):
            update.email = expense[i]
        elif (i == 'description'):
            update.description = expense[i]
        elif (i == 'link'):
            update.link = expense[i]
        elif (i == 'submit_date'):
            update.submit_date = expense[i]
        elif (i == 'status'):
            update.status = expense[i]
        elif (i == 'decision_date'):
            update.decision_date = expense[i]

    db1.session.commit()
    resp = Response(response=None,
                    status=202,
                    mimetype="application/text")
    return resp



port = 4000
host = '0.0.0.0'
r = redis.Redis('127.0.0.1', 6379)
r.rpush('activeServer', host + ":" + str(port))
app.run(debug=True, host=host, port=port)