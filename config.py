"""

Если проект запускается с помощью docker, то необходимо заменить:

логин - login - на тот который указали в docker-compose.yml
пароль - password -  на тот который указали в docker-compose.yml
хост - db -либо на IP либо на db который указан в docker-compose.yml
базу данных - database - на тот который указан в docker-compose.yml

"""

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://login:password@db/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'
    WTF_CSRF_SECRET_KEY = 'wtf_secret_key'
