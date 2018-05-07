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
	print(request.data)
	user_id = request.args.get("userid")
	results = rank_friends(user_id, M)
	print(results)
	return jsonify(influence_list=results)

@app.route('/sort', methods = ['GET'])
@crossdomain(origin='*')
def get_influences():
	userids = json.loads(request.args.get("userids"))
	print(userids)
	results = sort_list(userids, M)
	print(results)
	return jsonify(influence_list=results)
if __name__ == '__main__':
    app.run()
