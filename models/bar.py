"""
Modelo para los bares/establecimientos.
"""
from models.db import db
import logging

logger = logging.getLogger(__name__)

class Bar(db.Model):
    __tablename__ = 'bars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Horarios
    opening_time = db.Column(db.String(10), nullable=True)  # ej: "22:00"
    closing_time = db.Column(db.String(10), nullable=True)  # ej: "04:00"
    
    # Precios
    min_price = db.Column(db.Integer, nullable=True)  # en pesos
    max_price = db.Column(db.Integer, nullable=True)
    
    # Ubicación
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    
    # Géneros musicales (JSON string)
    music_genres = db.Column(db.Text, nullable=True)  # ["Reggaetón", "Electrónica"]
    
    # Rating
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    
    # Estado
    is_active = db.Column(db.Boolean, default=True)
    
    # Relaciones
    reservations = db.relationship('Reservation', backref='bar', lazy=True)
    availabilities = db.relationship('Availability', backref='bar', lazy=True)

    def __repr__(self):
        return f'<Bar {self.name}>'

    def to_dict(self):
        """Devuelve los datos del bar en formato JSON."""
        import json
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "description": self.description,
            "image_url": self.image_url,
            "phone": self.phone,
            "opening_time": self.opening_time,
            "closing_time": self.closing_time,
            "min_price": self.min_price,
            "max_price": self.max_price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "music_genres": json.loads(self.music_genres) if self.music_genres else [],
            "rating": self.rating,
            "total_reviews": self.total_reviews,
            "is_active": self.is_active
        }