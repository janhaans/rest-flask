class User():
    def __init__(self, id, name, password):
        self.id = id
        self.username = name
        self.password = password
    
    def __str__(self):
        return f'User(id={self.id})'

users = [
    User(1, 'user1', 'passwd1'),
    User(2, 'user2', 'passwd2')
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}