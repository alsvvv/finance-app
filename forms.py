from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired

# Форма для создания отчета
class ReportForm(FlaskForm):
    start_date = DateField('С', validators=[DataRequired()])  # Дата начала периода
    end_date = DateField('По', validators=[DataRequired()])  # Дата окончания периода
    transaction_type = SelectField('Тип транзакции', choices=[('income', 'Доход'), ('expense', 'Расход'),
                                                              ('both', 'Доход/Расход')], validators=[DataRequired()])  # Тип транзакции
    file_format = SelectField('Формат файла', choices=[('csv', 'CSV'), ('excel', 'Excel')],
                              validators=[DataRequired()])  # Формат файла отчета
    submit = SubmitField('Формировать отчёт')  # Кнопка отправки формы

# Форма для авторизации пользователя
class LoginForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired()])  # Поле для ввода логина
    password = PasswordField('Пароль', validators=[DataRequired()])  # Поле для ввода пароля
    submit = SubmitField('Авторизоваться')  # Кнопка отправки формы

# Форма для регистрации нового пользователя
class RegistrationForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired()])  # Поле для ввода логина
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email()])  # Поле для ввода email
    password = PasswordField('Введите пароль', validators=[DataRequired()])  # Поле для ввода пароля
    password2 = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password')])  # Поле для повторного ввода пароля
    submit = SubmitField('Зарегистрироваться')  # Кнопка отправки формы

    # Валидация уникальности логина
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')

    # Валидация уникальности email
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой адрес эл.почты.')

# Форма для изменения настроек пользователя
class SettingsForm(FlaskForm):
    email = StringField('Адрес электронной почты', render_kw={'readonly': True})  # Поле для email (только чтение)
    username = StringField('Логин пользователя', validators=[DataRequired()])  # Поле для ввода логина
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])  # Поле для ввода текущего пароля
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])  # Поле для ввода нового пароля
    new_password2 = PasswordField('Подтверждение нового пароля', validators=[
        DataRequired(), EqualTo('new_password')])  # Поле для повторного ввода нового пароля
    submit = SubmitField('Сохранить изменения')  # Кнопка отправки формы

