from flask import Flask, render_template, redirect, url_for, flash, request, send_file
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_migrate import Migrate
from forms import LoginForm, RegistrationForm, SettingsForm, ReportForm
from models import db, User, Transaction, Category
import pandas as pd
import io
from datetime import datetime

# Создаем объект приложения Flask
app = Flask(__name__)
# Загружаем конфигурацию приложения
app.config.from_object('config.Config')

# Инициализируем базу данных с приложением
db.init_app(app)
# Настраиваем миграции базы данных
migrate = Migrate(app, db)

# Инициализируем менеджер входа в систему
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Загрузка пользователя по его идентификатору
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Обработка маршрута /login для входа пользователей
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Неправильный логин или пароль', 'danger')
    return render_template('login.html', form=form)

# Обработка маршрута /register для регистрации новых пользователей
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Обработка маршрута /logout для выхода из системы
@app.route('/logout')
@login_required  # Требует аутентификации пользователя
def logout():
    logout_user()
    return redirect(url_for('login'))

# Обработка маршрута корневой страницы /
@app.route('/')
@login_required  # Требует аутентификации пользователя
def index():
    return render_template('index.html')

# Обработка маршрута /settings для изменения настроек пользователя
@app.route('/settings', methods=['GET', 'POST'])
@login_required  # Требует аутентификации пользователя
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        if not current_user.check_password(form.old_password.data):
            flash('Текущий пароль неверный.', 'danger')
        else:
            current_user.username = form.username.data
            if form.new_password.data:
                current_user.set_password(form.new_password.data)
            try:
                db.session.commit()
                flash('Изменения успешно сохранились.', 'success')
                return redirect(url_for('settings'))
            except Exception as e:
                db.session.rollback()
                flash(f'Ошибка при сохранении изменений: {str(e)}', 'danger')
    form.email.data = current_user.email
    form.username.data = current_user.username
    return render_template('settings.html', form=form)

# Обработка маршрута /transactions для просмотра транзакций
@app.route('/transactions')
@login_required  # Требует аутентификации пользователя
def view_transactions():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Transaction.query.filter_by(user_id=current_user.id)

    if start_date:
        query = query.filter(Transaction.date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Transaction.date <= datetime.strptime(end_date, '%Y-%m-%d'))

    transactions = query.all()
    return render_template('view_transactions.html', transactions=transactions)

# Обработка маршрута /transactions/add для добавления новой транзакции
@app.route('/transactions/add', methods=['GET', 'POST'])
@login_required  # Требует аутентификации пользователя
def add_transaction():
    if request.method == 'POST':
        transaction_type = request.form['type']
        amount = request.form['amount']
        currency = request.form['currency']
        date = request.form['date']
        category_name = request.form['category']

        category = Category.query.filter_by(name=category_name).first()
        if not category:
            category = Category(name=category_name)
            db.session.add(category)
            db.session.commit()

        transaction = Transaction(type=transaction_type, amount=amount, currency=currency, date=date,
                                  user_id=current_user.id, category_id=category.id)
        db.session.add(transaction)
        db.session.commit()
        flash('Транзакция успешно добавлена!', 'success')
        return redirect(url_for('view_transactions'))

    return render_template('add_transaction.html')

# Обработка маршрута /report для создания отчетов
@app.route('/report', methods=['GET', 'POST'])
@login_required  # Требует аутентификации пользователя
def report():
    form = ReportForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data
        transaction_type = form.transaction_type.data
        file_format = form.file_format.data

        query = Transaction.query.filter(Transaction.user_id == current_user.id, Transaction.date >= start_date,
                                         Transaction.date <= end_date)

        if transaction_type != 'both':
            query = query.filter(Transaction.type == transaction_type)

        transactions = query.all()

        data = [{
            'Дата': t.date,
            'Тип транзакции': 'Доход' if t.type == 'income' else 'Расход',
            'Сумма': t.amount,
            'Валюта': t.currency,
            'Категория': t.category.name
        } for t in transactions]

        df = pd.DataFrame(data)

        if file_format == 'csv':
            output = io.StringIO()
            df.to_csv(output, index=False)
            output.seek(0)
            return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True,
                             download_name='report.csv')
        else:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Report')
            output.seek(0)
            return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                             as_attachment=True, download_name='report.xlsx')

    return render_template('report.html', form=form)

# Запуск приложения Flask
if __name__ == '__main__':
    app.run(debug=True)

