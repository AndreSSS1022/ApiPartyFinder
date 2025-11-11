"""
Modelo para las reservas de usuarios.
"""
from models.db import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    bar_id = db.Column(db.Integer, db.ForeignKey('bars.id'), nullable=False)
    availability_id = db.Column(db.Integer, db.ForeignKey('availabilities.id'), nullable=True)
    
    # Datos de la reserva
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    num_people = db.Column(db.Integer, nullable=False)
    
    # Fecha y hora
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.String(10), nullable=False)
    
    # Estado
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, cancelled, completed
    
    # Notas
    notes = db.Column(db.Text, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    user = db.relationship('User', backref='reservations')

    def __repr__(self):
        return f'<Reservation {self.id} User:{self.user_id} Bar:{self.bar_id}>'

    def to_dict(self):
        """Devuelve los datos de la reserva en formato JSON."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "bar_id": self.bar_id,
            "bar_name": self.bar.name if self.bar else None,
            "bar_address": self.bar.address if self.bar else None,
            "bar_image": self.bar.image_url if self.bar else None,
            "full_name": self.full_name,
            "phone": self.phone,
            "num_people": self.num_people,
            "reservation_date": self.reservation_date.isoformat(),
            "reservation_time": self.reservation_time,
            "status": self.status,
            "notes": self.notes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }