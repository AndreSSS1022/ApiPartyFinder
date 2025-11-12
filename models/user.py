# models/user.py
from models.db import db
import logging

logger = logging.getLogger(__name__)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    birth_date = db.Column(db.Date, nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)  # URL o base64

    def __repr__(self):
        logger.info(f'Representación de usuario solicitada: {self.username}')
        return f'<User {self.username}>'

    def to_dict(self):
        """Devuelve los datos del usuario en formato JSON serializable."""
        return {
            "id": self.id,
            "username": self.username,
            "full_name": self.full_name,
            "birth_date": self.birth_date.isoformat() if self.birth_date else None,
            "profile_image": self.profile_image
        }
