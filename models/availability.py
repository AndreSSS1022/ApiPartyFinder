"""
Modelo para la disponibilidad de mesas por bar y fecha.
"""
from models.db import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Availability(db.Model):
    __tablename__ = 'availabilities'

    id = db.Column(db.Integer, primary_key=True)
    bar_id = db.Column(db.Integer, db.ForeignKey('bars.id'), nullable=False)
    
    # Fecha y hora
    date = db.Column(db.Date, nullable=False)
    time_slot = db.Column(db.String(10), nullable=False)  # ej: "22:00", "23:00"
    
    # Capacidad
    total_capacity = db.Column(db.Integer, nullable=False, default=10)
    reserved_count = db.Column(db.Integer, default=0)
    
    # Estado
    is_available = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Availability Bar:{self.bar_id} Date:{self.date} Slot:{self.time_slot}>'

    @property
    def available_capacity(self):
        """Retorna la capacidad disponible."""
        return self.total_capacity - self.reserved_count

    def to_dict(self):
        """Devuelve los datos en formato JSON."""
        return {
            "id": self.id,
            "bar_id": self.bar_id,
            "date": self.date.isoformat(),
            "time_slot": self.time_slot,
            "total_capacity": self.total_capacity,
            "reserved_count": self.reserved_count,
            "available_capacity": self.available_capacity,
            "is_available": self.is_available,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }