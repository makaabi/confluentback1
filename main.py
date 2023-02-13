from app import app, mongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import jsonify, flash, request
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/testapi')
def testapi():
	return "API Working"


@app.route('/weather/<city>',methods=['GET'])
def weatherbycity(city):
	return city

@app.route('/users',methods=['GET'])
def users():
	users = mongo.db.user.find()
	resp = dumps(users)
	print(resp)
	return resp

@app.route('/users/add',methods=['POST'])
def add_user():
	print("test1")
	_json = request.json
	_nom = _json['nom']
	_prenom = _json['prenom']
	_email = _json['email']
	_password = _json['pwd']
	if _nom and _prenom and _email and _password and request.method == 'POST':
		_hashed_password = generate_password_hash(_password)
		id = mongo.db.user.insert_one({'nom': _nom,'prenom': _prenom, 'email': _email, 'pwd': _hashed_password})
		resp = jsonify('User added successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		

		
@app.route('/user/<id>',methods=['GET'])
def user(id):
	user = mongo.db.user.find_one({'_id': ObjectId(id)})
	resp = dumps(user)
	return resp

@app.route('/user/update', methods=['PUT'])
def update_user():
	_json = request.json
	_id = _json['_id']
	_nom = _json['nom']
	_prenom = _json['prenom']
	_email = _json['email']
	_password = _json['pwd']		

	if _nom and _prenom and _email and _password and _id and request.method == 'PUT':
		_hashed_password = generate_password_hash(_password)
		mongo.db.user.update_one({'_id': ObjectId(_id['$oid']) if '$oid' in _id else ObjectId(_id)}, {'$set': {'nom': _nom,'prenom': _prenom, 'email': _email, 'pwd': _hashed_password}})
		resp = jsonify('User updated successfully!')
		resp.status_code = 200
		return resp
	else:
		return not_found()
		
@app.route('/user/delete/<id>', methods=['DELETE'])
def delete_user(id):
	mongo.db.user.delete_one({'_id': ObjectId(id)})
	resp = jsonify('User deleted successfully!')
	resp.status_code = 200
	return resp

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    app.run()
