from flask_mysqldb import MySQL

mysql = MySQL()

def init_app(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_PORT'] = 3309
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = '12345'
    app.config['MYSQL_DB'] = 'beauty_trainer'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

    mysql.init_app(app)
