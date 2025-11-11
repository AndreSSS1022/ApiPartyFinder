"""
Controlador para bares/establecimientos.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models.bar import Bar
from models.db import db
import logging
import json

logger = logging.getLogger(__name__)

bar_bp = Blueprint('bar_bp', __name__, url_prefix='/bars')


@bar_bp.route('/', methods=['GET'])
def get_bars():
    """
    Listar todos los bares activos
    ---
    tags:
      - Bares
    responses:
      200:
        description: Lista de bares
        schema:
          type: array
          items:
            type: object
    """
    try:
        bars = Bar.query.filter_by(is_active=True).all()
        return jsonify([bar.to_dict() for bar in bars]), 200
    except Exception as e:
        logger.error(f"Error al obtener bares: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bar_bp.route('/<int:bar_id>', methods=['GET'])
def get_bar(bar_id):
    """
    Obtener detalles de un bar
    ---
    tags:
      - Bares
    parameters:
      - in: path
        name: bar_id
        type: integer
        required: true
    responses:
      200:
        description: Detalles del bar
      404:
        description: Bar no encontrado
    """
    try:
        bar = Bar.query.get(bar_id)
        if not bar:
            return jsonify({"error": "Bar no encontrado"}), 404
        return jsonify(bar.to_dict()), 200
    except Exception as e:
        logger.error(f"Error al obtener bar: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bar_bp.route('/', methods=['POST'])
@jwt_required()
def create_bar():
    """
    Crear un nuevo bar
    ---
    tags:
      - Bares
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
          required: [name, address]
          properties:
            name:
              type: string
              example: "Dakiti Club"
            address:
              type: string
              example: "Carrera 22 #52, Bogotá"
            description:
              type: string
            image_url:
              type: string
            phone:
              type: string
            opening_time:
              type: string
              example: "22:00"
            closing_time:
              type: string
              example: "04:00"
            min_price:
              type: integer
            max_price:
              type: integer
            latitude:
              type: number
            longitude:
              type: number
            music_genres:
              type: array
              items:
                type: string
              example: ["Reggaetón", "Crossover"]
    responses:
      201:
        description: Bar creado exitosamente
      400:
        description: Datos inválidos
    """
    try:
        data = request.get_json() or {}
        
        if not data.get('name') or not data.get('address'):
            return jsonify({"error": "name y address son requeridos"}), 400
        
        # Convertir music_genres a JSON string
        music_genres = data.get('music_genres', [])
        if isinstance(music_genres, list):
            music_genres = json.dumps(music_genres)
        
        bar = Bar(
            name=data['name'],
            address=data['address'],
            description=data.get('description'),
            image_url=data.get('image_url'),
            phone=data.get('phone'),
            opening_time=data.get('opening_time'),
            closing_time=data.get('closing_time'),
            min_price=data.get('min_price'),
            max_price=data.get('max_price'),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            music_genres=music_genres
        )
        
        db.session.add(bar)
        db.session.commit()
        
        logger.info(f"Bar creado: {bar.name} (ID: {bar.id})")
        return jsonify(bar.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al crear bar: {str(e)}")
        return jsonify({"error": str(e)}), 500


@bar_bp.route('/<int:bar_id>', methods=['PUT'])
@jwt_required()
def update_bar(bar_id):
    """
    Actualizar un bar
    ---
    tags:
      - Bares
    security:
      - Bearer: []
    parameters:
      - in: path
        name: bar_id
        type: integer
        required: true
    responses:
      200:
        description: Bar actualizado
      404:
        description: Bar no encontrado
    """
    try:
        bar = Bar.query.get(bar_id)
        if not bar:
            return jsonify({"error": "Bar no encontrado"}), 404
        
        data = request.get_json() or {}
        
        # Actualizar campos
        for field in ['name', 'address', 'description', 'image_url', 'phone',
                     'opening_time', 'closing_time', 'min_price', 'max_price',
                     'latitude', 'longitude', 'is_active']:
            if field in data:
                setattr(bar, field, data[field])
        
        if 'music_genres' in data:
            music_genres = data['music_genres']
            if isinstance(music_genres, list):
                music_genres = json.dumps(music_genres)
            bar.music_genres = music_genres
        
        db.session.commit()
        logger.info(f"Bar actualizado: {bar.name}")
        return jsonify(bar.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error al actualizar bar: {str(e)}")
        return jsonify({"error": str(e)}), 500