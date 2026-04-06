from flask_login import UserMixin
from werkzeug.security import check_password_hash

class Usuario(UserMixin):
    def __init__(self, id_usuario, nombre, email, password_hash):
        self.id = id_usuario   # Flask-Login usa self.id
        self.nombre = nombre
        self.email = email
        self.password_hash = password_hash

    def verificar_password(self, password):
        return check_password_hash(self.password_hash, password)