from flask import Flask, jsonify
from flask import request
from DB_shard1 import db
from DB_shard1 import ExpenseSchema
from DB_shard1 import CreateDB


app = Flask(__name__)
CreateDB()
db.create_all()

@app.route('/v1/expenses/<int:expenses_id>', methods = ['GET'])
def handle_get(expenses_id):
	user = ExpenseSchema.query.filter_by(id = expenses_id).first_or_404()
	return jsonify({ 'id': user.id, 'name': user.name, 'email': user.email , 'category': user.category, 'description': user.description, 'link': user.link ,
					 'estimated_costs': user.estimated_costs, 'submit_date':user.submit_date , 'status': user.status, 'decision_date': user.decision_date})


@app.route('/v1/expenses' , methods=['POST'])
def handle_post():
	object=request.get_json(force=True)
	user = ExpenseSchema(object['id'], object['name'], object['email'], object['category'], object['description'], object['link'], object['estimated_costs'], object['submit_date'], 'pending', '09-10-2016')
	db.session.add(user)
	db.session.commit()
	return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'category': user.category,
					'description': user.description, 'link': user.link,
					'estimated_costs': user.estimated_costs, 'submit_date': user.submit_date, 'status': user.status,
					'decision_date':user.decision_date}), 201

@app.route('/v1/expenses/<expenses_id>' ,methods=['PUT'])
def handle_put(expenses_id):
	object1 = request.get_json(force=True)
	user = ExpenseSchema.query.filter_by(id=expenses_id).first_or_404()
	user.estimated_costs=object1['estimated_costs']
	db.session.commit()
	return jsonify({}), 202





@app.route('/v1/expenses/<expenses_id>' ,methods=['DELETE'])
def handle_delete(expenses_id):
	user = ExpenseSchema.query.filter_by(id=expenses_id).first_or_404()
	db.session.delete(user)
	db.session.commit()

	return jsonify({}), 204



if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8001, debug=True)



