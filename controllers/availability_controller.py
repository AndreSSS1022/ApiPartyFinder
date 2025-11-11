"""
Controlador para gestionar la disponibilidad de los bares.
Panel de administración para configurar horarios y capacidad.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from services.availability_service import AvailabilityService
import logging

logger = logging.getLogger(__name__)

availability_bp = Blueprint('availability_bp', __name__, url_prefix='/availability')


@availability_bp.route('/', methods=['POST'])
@jwt_required()
def create_availability():
    """
    Crear o actualizar disponibilidad
    ---
    tags:
      - Disponibilidad
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
          required: [bar_id, date, time_slot, total_capacity]
          properties:
            bar_id:
              type: integer
              example: 1
            date:
              type: string
              format: date
              example: "2024-11-15"
            time_slot:
              type: string
              example: "22:00"
            total_capacity:
              type: integer
              example: 20
            is_available:
              type: boolean
              example: true
    responses:
      201:
        description: Disponibilidad creada/actualizada
      400:
        description: Datos inválidos
      401:
        description: No autenticado
    """
    try:
        data = request.get_json() or {}
        
        required = ['bar_id', 'date', 'time_slot', 'total_capacity']
        if not all(field in data for field in required):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        result = AvailabilityService.create_or_update_availability(
            bar_id=data['bar_id'],
            date=data['date'],
            time_slot=data['time_slot'],
            total_capacity=data['total_capacity'],
            is_available=data.get('is_available', True)
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en create_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500


@availability_bp.route('/bulk', methods=['POST'])
@jwt_required()
def create_bulk_availability():
    """
    Crear disponibilidad para múltiples días
    ---
    tags:
      - Disponibilidad
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
          required: [bar_id]
          properties:
            bar_id:
              type: integer
              example: 1
            days:
              type: integer
              example: 7
              description: Número de días hacia adelante
            time_slots:
              type: array
              items:
                type: string
              example: ["22:00", "23:00", "00:00"]
            capacity:
              type: integer
              example: 20
    responses:
      201:
        description: Disponibilidades creadas
      401:
        description: No autenticado
    """
    try:
        data = request.get_json() or {}
        
        if 'bar_id' not in data:
            return jsonify({"error": "bar_id es requerido"}), 400
        
        result = AvailabilityService.create_weekly_availability(
            bar_id=data['bar_id'],
            days=data.get('days', 7),
            time_slots=data.get('time_slots'),
            capacity=data.get('capacity', 20)
        )
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        logger.error(f"Error en create_bulk_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500


@availability_bp.route('/bar/<int:bar_id>', methods=['GET'])
def get_bar_availability(bar_id):
    """
    Obtener disponibilidad de un bar
    ---
    tags:
      - Disponibilidad
    parameters:
      - in: path
        name: bar_id
        type: integer
        required: true
      - in: query
        name: start_date
        type: string
        format: date
        example: "2024-11-10"
      - in: query
        name: end_date
        type: string
        format: date
        example: "2024-11-17"
    responses:
      200:
        description: Lista de disponibilidades
        schema:
          type: array
          items:
            type: object
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        availabilities = AvailabilityService.get_bar_availability(
            bar_id, start_date, end_date
        )
        return jsonify(availabilities), 200
        
    except Exception as e:
        logger.error(f"Error en get_bar_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500


@availability_bp.route('/<int:availability_id>', methods=['DELETE'])
@jwt_required()
def delete_availability(availability_id):
    """
    Eliminar una disponibilidad
    ---
    tags:
      - Disponibilidad
    security:
      - Bearer: []
    parameters:
      - in: path
        name: availability_id
        type: integer
        required: true
    responses:
      200:
        description: Disponibilidad eliminada
      400:
        description: No se puede eliminar (tiene reservas)
      401:
        description: No autenticado
    """
    try:
        result = AvailabilityService.delete_availability(availability_id)
        
        if 'error' in result:
            return jsonify(result), 400
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error en delete_availability: {str(e)}")
        return jsonify({"error": str(e)}), 500