"""
Servicio para manejar la lógica de reservas.
"""
from models.db import db
from models.reservation import Reservation
from models.availability import Availability
from models.bar import Bar
from models.user import User
from services.email_service import EmailService
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class ReservationService:
    
    @staticmethod
    def create_reservation(user_id: int, bar_id: int, full_name: str, phone: str, 
                          num_people: int, reservation_date: str, reservation_time: str,
                          notes: str = None) -> dict:
        """
        Crea una nueva reserva y actualiza la disponibilidad.
        
        Returns:
            dict: Datos de la reserva creada o error
        """
        try:
            # Validar que el bar existe
            bar = Bar.query.get(bar_id)
            if not bar:
                return {"error": "Bar no encontrado"}
            
            # Buscar disponibilidad
            date_obj = datetime.strptime(reservation_date, '%Y-%m-%d').date()
            availability = Availability.query.filter_by(
                bar_id=bar_id,
                date=date_obj,
                time_slot=reservation_time
            ).first()
            
            # Si no existe disponibilidad, crearla automáticamente
            if not availability:
                availability = Availability(
                    bar_id=bar_id,
                    date=date_obj,
                    time_slot=reservation_time,
                    total_capacity=20,  # Capacidad por defecto
                    reserved_count=0
                )
                db.session.add(availability)
                db.session.flush()
            
            # Verificar capacidad
            if availability.reserved_count >= availability.total_capacity:
                return {"error": "No hay disponibilidad para esta fecha y hora"}
            
            # Crear la reserva
            reservation = Reservation(
                user_id=user_id,
                bar_id=bar_id,
                availability_id=availability.id,
                full_name=full_name,
                phone=phone,
                num_people=num_people,
                reservation_date=date_obj,
                reservation_time=reservation_time,
                status='confirmed',
                notes=notes
            )
            
            # Actualizar disponibilidad
            availability.reserved_count += 1
            if availability.reserved_count >= availability.total_capacity:
                availability.is_available = False
            
            db.session.add(reservation)
            db.session.commit()
            
            logger.info(f"Reserva creada: {reservation.id} para usuario {user_id}")
            
            # Enviar email de confirmación
            user = User.query.get(user_id)
            if user and hasattr(user, 'username'):
                reservation_data = reservation.to_dict()
                # Intentar enviar email (no bloquear si falla)
                try:
                    EmailService.send_reservation_confirmation(
                        reservation_data, 
                        user.username  # Asumiendo que username es el email
                    )
                except Exception as e:
                    logger.warning(f"No se pudo enviar email: {str(e)}")
            
            return reservation.to_dict()
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al crear reserva: {str(e)}")
            return {"error": str(e)}
    
    @staticmethod
    def get_user_reservations(user_id: int) -> list:
        """Obtiene todas las reservas de un usuario."""
        try:
            reservations = Reservation.query.filter_by(user_id=user_id).order_by(
                Reservation.reservation_date.desc()
            ).all()
            return [r.to_dict() for r in reservations]
        except Exception as e:
            logger.error(f"Error al obtener reservas: {str(e)}")
            return []
    
    @staticmethod
    def get_bar_reservations(bar_id: int) -> list:
        """Obtiene todas las reservas de un bar (para admin)."""
        try:
            reservations = Reservation.query.filter_by(bar_id=bar_id).order_by(
                Reservation.reservation_date.desc()
            ).all()
            return [r.to_dict() for r in reservations]
        except Exception as e:
            logger.error(f"Error al obtener reservas del bar: {str(e)}")
            return []
    
    @staticmethod
    def cancel_reservation(reservation_id: int, user_id: int) -> dict:
        """Cancela una reserva y libera la disponibilidad."""
        try:
            reservation = Reservation.query.get(reservation_id)
            
            if not reservation:
                return {"error": "Reserva no encontrada"}
            
            if reservation.user_id != user_id:
                return {"error": "No autorizado"}
            
            # Actualizar disponibilidad
            if reservation.availability_id:
                availability = Availability.query.get(reservation.availability_id)
                if availability:
                    availability.reserved_count = max(0, availability.reserved_count - 1)
                    availability.is_available = True
            
            reservation.status = 'cancelled'
            db.session.commit()
            
            logger.info(f"Reserva cancelada: {reservation_id}")
            return {"message": "Reserva cancelada exitosamente"}
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error al cancelar reserva: {str(e)}")
            return {"error": str(e)}