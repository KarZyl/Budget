from flask import Flask, jsonify, abort, make_response, request
from models import budget

app = Flask(__name__)
app.config["SECRET_KEY"] = "nininini"

@app.route("/api/v1/budget/", methods=["GET"])
def budget_list_api_v1():
    return jsonify(budget.all())

@app.route("/api/v1/budget/", methods=["POST"])
def create_item():
    if not request.json or not 'title' in request.json:
        abort(400)
    item = {
        'id': budget.all()[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'value': request.json['value']
    }
    budget.create(item)
    return jsonify({'item': item}), 201

@app.route("/api/v1/budget/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = budget.get(item_id)
    if not item:
        abort(404)
    return jsonify({"item": item})

@app.route("/api/v1/budget/<int:item_id>", methods=['DELETE'])
def delete_item(item_id):
    result = budget.delete(item_id)
    if not result:
        abort(404)
    return jsonify({'result': result})

@app.route("/api/v1/budget/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = budget.get(item_id)
    if not item:
        abort(404)
    if not request.json:
        abort(400)
    data = request.json
    if any([
        'title' in data and not isinstance(data.get('title'), str),
        'description' in data and not isinstance(data.get('description'), str),
        'value' in data and not isinstance(data.get('value'), float or int)
    ]):
        abort(400)
    item = {
        'title': data.get('title', item['title']),
        'description': data.get('description', item['description']),
        'value': data.get('value', item['value'])
    }
    budget.update(item_id, item)
    return jsonify({'item': item})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found', 'status_code': 404}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request', 'status_code': 400}), 400)

if __name__ == "__main__":
    app.run(debug=True)