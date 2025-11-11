"""
Servicio para gestionar la disponibilidad de los bares.
"""
from models.db import db
from models.availability import Availability
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AvailabilityService:
    
    @staticmethod
    def create_or_update_availability(bar_id: int, date: str, time_slot: str, 
                                     total_capacity: int, is_available: bool = True) -> dict:
        """
        Crea o actualiza la disponibilidad para un bar en una fecha/hora específica.
        """
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date()
            
            # Buscar disponibilidad existente
            availability = Availability.query.filter_by(
                bar_id=bar_id,
                date=date_obj,
                time_slot=time_slot
            ).first()
            
            if availability:
                # Actualizar existente
                availability.total_capacity = total_capacity
                availability.is_available = is_available
                availability.updated_at = datetime.utcnow()
                logger.info(f"Disponibilidad actualizada: Bar {bar_id}, {date}, {time_slot}")
            else:
                # Crear nueva
                availability = Availability(
                    bar_id=bar_id,
                    date=date_obj,
                    time_slot=time_slot,
                    total_capacity=total_capacity,
                    reserved_count=0,
                    is_available=is_available
                )
                db.session.add(availability)
                logger.info(f"Disponibilidad creada: Bar {bar_id}, {date}, {time_slot}")
            
            db.session.commit()
            return availability.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear/actualizar disponibilidad: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def create_weekly_availability(bar_id: int, days: int = 7, time_slots: list = None, 
                                  capacity: int = 20) -> dict:
        """
        Crea disponibilidad automática para los próximos N días.
        
        Args:
            bar_id: ID del bar
            days: Número de días hacia adelante
            time_slots: Lista de horarios (ej: ["22:00", "23:00", "00:00"])
            capacity: Capacidad por slot
        """
        try:
            if not time_slots:
                time_slots = ["22:00", "23:00", "00:00", "01:00"]
            
            created_count = 0
            start_date = datetime.now().date()
            
            for day in range(days):
                current_date = start_date + timedelta(days=day)
                
                for time_slot in time_slots:
                    # Verificar si ya existe
                    exists = Availability.query.filter_by(
                        bar_id=bar_id,
                        date=current_date,
                        time_slot=time_slot
                    ).first()
                    
                    if not exists:
                        availability = Availability(
                            bar_id=bar_id,
                            date=current_date,
                            time_slot=time_slot,
                            total_capacity=capacity,
                            reserved_count=0,
                            is_available=True
                        )
                        db.session.add(availability)
                        created_count += 1
            
            db.session.commit()
            logger.info(f"Creadas {created_count} disponibilidades para bar {bar_id}")
            return {"message": f"Creadas {created_count} disponibilidades", "count": created_count}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear disponibilidad semanal: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def get_bar_availability(bar_id: int, start_date: str = None, end_date: str = None) -> list:
        """
        Obtiene la disponibilidad de un bar en un rango de fechas.
        """
        try:
            query = Availability.query.filter_by(bar_id=bar_id)
            
            if start_date:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                query = query.filter(Availability.date >= start)
            
            if end_date:
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                query = query.filter(Availability.date <= end)
            
            availabilities = query.order_by(Availability.date, Availability.time_slot).all()
            return [a.to_dict() for a in availabilities]
            
        except Exception as e:
            logger.error(f"Error al obtener disponibilidad: {str(e)}")
            return []
    
    @staticmethod
    def delete_availability(availability_id: int) -> dict:
        """Elimina una disponibilidad (solo si no tiene reservas)."""
        try:
            availability = Availability.query.get(availability_id)
            
            if not availability:
                return {"error": "Disponibilidad no encontrada"}
            
            if availability.reserved_count > 0:
                return {"error": "No se puede eliminar: tiene reservas activas"}
            
            db.session.delete(availability)
            db.session.commit()
            
            logger.info(f"Disponibilidad eliminada: {availability_id}")
            return {"message": "Disponibilidad eliminada exitosamente"}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al eliminar disponibilidad: {str(e)}")
            return {"error": str(e)}