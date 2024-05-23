from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# Создаем объект базы данных SQLAlchemy
db = SQLAlchemy()

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор пользователя
    username = db.Column(db.String(80), unique=True, nullable=False)  # Имя пользователя, должно быть уникальным
    email = db.Column(db.String(120), unique=True, nullable=False)  # Электронная почта, должна быть уникальной
    password_hash = db.Column(db.String(256), nullable=False)  # Хеш пароля пользователя
    transactions = db.relationship('Transaction', backref='user', lazy=True)  # Связь с транзакциями пользователя

    # Установка пароля пользователя
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Проверка пароля пользователя
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Модель категории транзакций
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор категории
    name = db.Column(db.String(50), unique=True, nullable=False)  # Название категории, должно быть уникальным
    transactions = db.relationship('Transaction', backref='category', lazy=True)  # Связь с транзакциями категории

# Модель транзакции
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Уникальный идентификатор транзакции
    type = db.Column(db.String(10), nullable=False)  # Тип транзакции ('income' или 'expense')
    amount = db.Column(db.Float, nullable=False)  # Сумма транзакции
    currency = db.Column(db.String(10), nullable=False)  # Валюта транзакции ('RUB', 'EUR', 'USD')
    date = db.Column(db.Date, nullable=False)  # Дата транзакции
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Идентификатор пользователя
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)  # Идентификатор категории

