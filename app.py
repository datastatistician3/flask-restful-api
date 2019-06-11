from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api
from flask_pymongo import PyMongo
import pymongo
from flask_sqlalchemy import SQLAlchemy
import os
import json

app = Flask(__name__)
api =Api(app)

# app.config['MONGO_URI'] = "mongodb+srv://som:myapp123%23%@cluster0-wpidj.mongodb.net/test?retryWrites=true&w=majority"

# mongo = pymongo.MongoClient('mongodb+srv://som:myapp123%23%@cluster0-wpidj.mongodb.net/test?retryWrites=true&w=majority', maxPoolSize=50, connect=False)
# db = pymongo.database.Database(mongo, 'connect')
# col = pymongo.collection.Collection(db, 'users')

# mongo = PyMongo(app)

app.config['SECRET_KEY'] = 'mysecrets'
app.config['SQLALCHEMY_DATABASE_URI'] = './myapidb.db' #'mysql+pymysql://' + db_creds['mysql_user'] + ':' + db_creds['mysql_pasword'] + '@' + db_creds['mysql_host'] + '/' + db_creds['mysql_db']

db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String())
#     language = db.Column(db.String())

# @app.route('/framework', methods =['GET'])
# def get_all_frameworks():
#     framework = User.query.all()
#     print(framework)

#     output = []

#     for q in framework.name:
#         output.append({'name': q['name'], 'language': q['language']})

#     return jsonify({'result': output})


# @app.route('/')
# def show_all():
#    return render_template('show_all.html', students = User.query.all() )

@app.route('/', methods=['POST', 'GET'])
# curl -H "Content-Type: application/json" -X POST -d '{"name":"xny","address":"fdsf"}'  http://127.0.0.1:5000/
def index():
	if request.method == 'POST':
		some_json = request.get_json()
		return jsonify({'You sent' : some_json}), 201
	else:
		return jsonify({'about': "You did not pass any JSON."})

@app.route('/hello')
def hello():
	return jsonify({'result': "Hello World"})

@app.route('/multi/<int:num>', methods=['GET'])
def get_multi(num):
	return jsonify({'result': num *10})

@app.route('/post/<namesage>', methods=['GET'])
# curl http://127.0.0.1:5000/post/shyam+43
def post(namesage):
	names = namesage.split('+')
	values = {'names': names[0].split(','), 'age': names[1].split(',')}
	filename = 'vault.json'
	exists = os.path.isfile(filename)
	try:
		if not exists:
			with open(filename, 'w') as fd:
				json.dump({'data': [values]}, fd)

		elif exists:
			with open(filename, 'r') as f:
				data = json.load(f)
			data.get('data').append([values])

			with open(filename, 'w') as fd:
				json.dump(data, fd)
		return("Data successfully written to JSON file called "+ filename)
	except ValueError:
		return("Could not write to JSON file.")

@app.route('/get_names')
def get_names():
	filename = 'vault.json'
	exists = os.path.isfile(filename)

	try:
		with open(filename, 'r') as f:
			data1 = json.load(f)
	except ValueError:
		print(filename, " does not exists.")
	d1 = data1.get('data')
	return jsonify({'data': d1})


# RESTFul API using flask_restful

class HelloWorld(Resource):
		def get(self):
			return {'about': "Hello World"}
		def post(self):
			some_json = request.get_json()
			return {'you sent ': some_json}

class Multi(Resource):
    	def get(self, num):
    		return {'result': num*10}

api.add_resource(HelloWorld, '/')
api.add_resource(Multi, '/multi/<int:num>')

if __name__ == '__main__':
	app.run(debug=True)
