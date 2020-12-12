from flask import Flask, jsonify

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
    pass

#GET /store/<string:name>   Get store with name = name
@app.route('/store/<string:name>')
def get_store(name):
    pass

#GET /store     Get list of all stores
@app.route('/store')
def get_stores():
    return jsonify({'stores': stores})

#POST /store/<sting:name>/item  data:{name:,price:}     Create new item for store name = name
@app.route('/store/<string:name>/item', methods=['POST'])
def create_item_in_store(name):
    pass

#GET /store/<string:name>/item  Get all items of store with name = name
@app.route('/store/<string:name>/item')
def get_item_in_store(name):
    pass


app.run(host='0.0.0.0', port=5000)