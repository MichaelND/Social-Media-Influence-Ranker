from flask import Flask, json, jsonify, request, render_template
from crossdomain import crossdomain
from sort_friends import *
from train import model

app = Flask(__name__)
M = model()

@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/influence', methods = ['GET'])
@crossdomain(origin='*')
def get_influence():
	user_id = request.args.get("userid")
	print(request.data)
	results = rank_friends(user_id, M)
	print(results)
	return jsonify(influence_list=results)