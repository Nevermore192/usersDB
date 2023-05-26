from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Указываем URI для подключения к базе данных
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Инициализируем объект миграции

# Модель данных пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }

# Маршрут для получения информации о всех пользователях
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_dict = [user.to_dict() for user in users]
    return jsonify(users_dict)

# Маршрут для получения информации о конкретном пользователе
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run()
