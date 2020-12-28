import sqlite3

class ItemModel():
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def get_item(cls, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items WHERE name=?'
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()
        if row:
            return cls(*row)

    def create_item(self):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'INSERT INTO items VALUES (?, ?)'
        cursor.execute(query, (self.name, self.price))
        connection.commit()
        connection.close()

    def update_item(self):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()

    @classmethod
    def delete_item(cls, name):
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        connection.commit()
        connection.close()

    @classmethod
    def get_items(cls):
        items = []
        connection = sqlite3.connect('data/data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM items'
        results = cursor.execute(query)
        for row in results:
            item = cls(*row)
            items.append(item.json())
        connection.close()
        return items

    