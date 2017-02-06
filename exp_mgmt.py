from flask import Flask, jsonify, request, Response, json
from flask_sqlalchemy import SQLAlchemy
from random import randint
from sqlalchemy import create_engine
from flask_script import Manager

app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@localhost/expense_mgmt_sys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
DATABASE='expense_mgmt_sys'

class ExpenseSystem(db.Model):
    __tablename__ = 'expense_sheet'

    expense_id = db.Column('expense_id',db.Integer, primary_key=True, nullable=False)
    name = db.Column('name',db.Unicode(25),nullable=False)
    email = db.Column('email',db.Unicode(40),nullable=False)
    category=db.Column('category',db.Unicode(100),nullable=False)
    description=db.Column('description',db.Unicode(100),nullable=False)
    link=db.Column('link',db.Unicode(100),nullable=False)
    estimated_costs=db.Column('estimated_costs',db.Unicode(10),nullable=False)
    submit_date=db.Column('submit_date',db.Unicode(10),nullable=False)
    status=db.Column('status',db.Unicode(50),nullable=False)
    decision_date=db.Column('decision_date',db.Unicode(50),nullable=False)
    
    def __init__(self,expense_id,name,email,category,description,link,status,estimated_costs,submit_date,decision_date):
        self.expense_id=expense_id
        self.category=category
        self.description=description
        self.name=name
        self.email=email
        self.link=link
        self.status=status
        self.decision_date=decision_date
        self.estimated_costs=estimated_costs
        self.submit_date=submit_date

@app.route('/v1/expenses',methods=['POST']) 
def expensePost():
    exp=request.get_json(force='True')
    name=exp["name"]
    email=exp['email']
    category=exp['category']
    description=exp['description']
    link=exp['link']
    submit_date=exp['submit_date']
    estimated_costs=exp['estimated_costs']
    status='pending'
    decision_date=''
    #code to generate random expense_id for each post request
    expense_id=randint(1000,9999)
    engine = create_engine("mysql://root:bhushan@localhost")
    engine.execute("CREATE DATABASE IF NOT EXISTS %s "%(DATABASE))
    engine.execute("USE %s "%(DATABASE))
    db.create_all()
    first_record=ExpenseSystem(expense_id,name,email,category,description,link,status,estimated_costs,submit_date,decision_date)
    db.session.add(first_record)
    db.session.commit()
    data={'id':str(expense_id),'name':name,'email':email,'category':category,'description':description,'link':link,'estimated_costs':estimated_costs,'submit_date':submit_date,'status':status,'decision_date':decision_date}  
    res = Response(response=json.dumps(data),
     status=201,
     mimetype="application/json")
    return res

@app.route('/v1/expenses/<string:expense_id>', methods=['GET'])
def getOneExpense(expense_id):
    #print "hello from GET"
    exp=ExpenseSystem.query.filter_by(expense_id=expense_id).first() 
    if exp == None:
         res = Response(response=None,status=404,mimetype="application/json")
         return res
    else:     
        data={'name':exp.name, 'email':exp.email,'category':exp.category,'description':exp.description,'link':exp.link,'estimated_costs':exp.estimated_costs,'submit_date':exp.submit_date,'status':exp.status,'decision_date':exp.decision_date}
        res = Response(response=json.dumps(data),status=200,mimetype="application/json")
        return res

@app.route('/v1/expenses/<string:expense_id>',methods=['DELETE'])
def deleteExpense(expense_id):
   # print "Hello from DElete"
  deleteObj=ExpenseSystem.query.filter_by(expense_id=expense_id).first()
  if deleteObj == None:
        result = Response(response=None,status=404,mimetype="application/json")
        return result  
  else:     
    db.session.delete(deleteObj)
    db.session.commit()
    result = Response(response=None,
    status=204,
    mimetype="application/text")
  return result 

@app.route('/v1/expenses/<string:expense_id>',methods=['PUT'])
def putExpense(expense_id):
    #print "Hello from PUT "
    exp=request.get_json(force='True')
    putUpdate=ExpenseSystem.query.filter_by(expense_id=expense_id).first()
    putUpdate.estimated_costs =exp.get("estimated_costs")
    db.session.commit()
    res = Response(response=None,
     status=202,
     mimetype="application/text")
    return res


if __name__ == "__main__":
    app.run(port=5000, debug=True)
