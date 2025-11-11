"""
Modelo de usuario para SQLAlchemy.
Puedes crear más modelos siguiendo este ejemplo y agregarlos en la carpeta models.
"""


from models.db import db
import logging

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)
    email= db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    birthdate= db.Column(db.Date, unique=True, nullable=False)

    def __repr__(self):
        logger.info(f'Representación de usuario solicitada: {self.email}')
        return f'<User {self.email}>'

"""
Para crear más modelos:
1. Crea un archivo en la carpeta models (ejemplo: product.py).
2. Define la clase heredando de db.Model.
3. Agrega los campos necesarios.
"""