from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    { 
        'name': 'My Store',
        'items': [
            {'name': 'my items', 'price': 15.99}
        ]
    }
]

#POST /store data:{name:}   Create new store with a name
@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    stores.append(new_store)
    return jsonify(new_store)

#GET /store/<string:name>   Get store with name = name
@app.route('/store/<string:name>')
def get_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'error': f'store with name {name} is not found'})

#GET /store     Get list of all stores
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

#POST /store/<sting:name>/item  data:{name:,price:}     Create new item for store name = name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            request_data = request.get_json()
            store['items'].append({'name': request_data['name'], 'price': request_data['price']})
            return jsonify({'message': f"item {request_data['name']} has been added to store {name}"})
    return jsonify({'error': f'store with name {name} is not found'})

#GET /store/<string:name>/item  Get all items of store with name = name
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'error': f'store with name {name} is not found'})


app.run(host='0.0.0.0', port=5000)