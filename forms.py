from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import User
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ReportForm(FlaskForm):
    start_date = DateField('С', validators=[DataRequired()])
    end_date = DateField('По', validators=[DataRequired()])
    transaction_type = SelectField('Тип транзакции', choices=[('income', 'Доход'), ('expense', 'Расход'),
                                                              ('both', 'Доход/Расход')], validators=[DataRequired()])
    file_format = SelectField('Формат файла', choices=[('csv', 'CSV'), ('excel', 'Excel')],
                              validators=[DataRequired()])
    submit = SubmitField('Формировать отчёт')


class LoginForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Авторизоваться')


class RegistrationForm(FlaskForm):
    username = StringField('Логин пользователя', validators=[DataRequired()])
    email = StringField('Адрес электронной почты', validators=[DataRequired(), Email()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    password2 = PasswordField('Подтвердите пароль', validators=[
        DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')


    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте другой логин.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Пожалуйста, используйте друго адрес эл.почты.')


class SettingsForm(FlaskForm):
    email = StringField('Адрес электронной почты', render_kw={'readonly': True})
    username = StringField('Логин пользователя', validators=[DataRequired()])
    old_password = PasswordField('Текущий пароль', validators=[DataRequired()])
    new_password = PasswordField('Новый пароль', validators=[DataRequired()])
    new_password2 = PasswordField('Подтверждение новой пароли', validators=[
        DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Сохранить изменения')
