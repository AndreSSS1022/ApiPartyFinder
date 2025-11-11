"""
Controlador para reservas.
Define los endpoints REST para crear, consultar y cancelar reservas.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.reservation_service import ReservationService
import logging

logger = logging.getLogger(__name__)

reservation_bp = Blueprint('reservation_bp', __name__, url_prefix='/reservations')


@reservation_bp.route('/', methods=['POST'])
@jwt_required()
def create_reservation():
    """
    Crear nueva reserva
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [bar_id, full_name, phone, num_people, reservation_date, reservation_time]
          properties:
            bar_id:
              type: integer
              example: 1
            full_name:
              type: string
              example: "Juan Pérez"
            phone:
              type: string
              example: "+57 300 1234567"
            num_people:
              type: integer
              example: 4
            reservation_date:
              type: string
              format: date
              example: "2024-11-15"
            reservation_time:
              type: string
              example: "22:00"
            notes:
              type: string
              example: "Mesa cerca de la pista"
    responses:
      201:
        description: Reserva creada exitosamente
      400:
        description: Datos inválidos
      401:
        description: No autenticado
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json() or {}
        
        # Validar campos requeridos
        required = ['bar_id', 'full_name', 'phone', 'num_people', 'reservation_date', 'reservation_time']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        result = ReservationService.create_reservation(
            user_id=user_id,
            bar_id=data['bar_id'],
            full_name=data['full_name'],
            phone=data['phone'],
            num_people=data['num_people'],
            reservation_date=data['reservation_date'],
            reservation_time=data['reservation_time'],
            notes=data.get('notes')
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en create_reservation: {str(e)}")
        return jsonify({"error": str(e)}), 500


@reservation_bp.route('/my-reservations', methods=['GET'])
@jwt_required()
def get_my_reservations():
    """
    Obtener mis reservas
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    responses:
      200:
        description: Lista de reservas del usuario
        schema:
          type: array
          items:
            type: object
      401:
        description: No autenticado
    """
    try:
        user_id = int(get_jwt_identity())
        reservations = ReservationService.get_user_reservations(user_id)
        return jsonify(reservations), 200
    except Exception as e:
        logger.error(f"Error en get_my_reservations: {str(e)}")
        return jsonify({"error": str(e)}), 500


@reservation_bp.route('/bar/<int:bar_id>', methods=['GET'])
@jwt_required()
def get_bar_reservations(bar_id):
    """
    Obtener reservas de un bar (para administradores)
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    parameters:
      - in: path
        name: bar_id
        type: integer
        required: true
    responses:
      200:
        description: Lista de reservas del bar
      401:
        description: No autenticado
    """
    try:
        # TODO: Agregar verificación de permisos de admin
        reservations = ReservationService.get_bar_reservations(bar_id)
        return jsonify(reservations), 200
    except Exception as e:
        logger.error(f"Error en get_bar_reservations: {str(e)}")
        return jsonify({"error": str(e)}), 500


@reservation_bp.route('/<int:reservation_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_reservation(reservation_id):
    """
    Cancelar una reserva
    ---
    tags:
      - Reservas
    security:
      - Bearer: []
    parameters:
      - in: path
        name: reservation_id
        type: integer
        required: true
    responses:
      200:
        description: Reserva cancelada exitosamente
      401:
        description: No autenticado
      404:
        description: Reserva no encontrada
    """
    try:
        user_id = int(get_jwt_identity())
        result = ReservationService.cancel_reservation(reservation_id, user_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Error en cancel_reservation: {str(e)}")
        return jsonify({"error": str(e)}), 500