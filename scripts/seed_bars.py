"""
Script para insertar los bares iniciales en la base de datos.
Ejecutar: python scripts/seed_bars.py
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models.bar import Bar
import json

def seed_bars():
    """Inserta los bares iniciales en la BD."""
    
    bars_data = [
        {
            "name": "Dakiti Club",
            "address": "Carrera 22 #52, Bogotá",
            "description": "Un club con ambiente crossover y la mejor música para bailar toda la noche.",
            "image_url": "https://example.com/dakiti.jpg",
            "phone": "+57 1 234 5678",
            "opening_time": "22:00",
            "closing_time": "04:00",
            "min_price": 30000,
            "max_price": 50000,
            "latitude": 4.6482,
            "longitude": -74.0577,
            "music_genres": json.dumps(["Reggaetón", "Crossover"]),
            "rating": 4.8,
            "total_reviews": 450
        },
        {
            "name": "Theatron",
            "address": "Calle 58 Bis #10 - 32, Bogotá",
            "description": "El club más grande de Latinoamérica, con múltiples ambientes y géneros.",
            "image_url": "https://example.com/theatron.jpg",
            "phone": "+57 1 345 6789",
            "opening_time": "21:00",
            "closing_time": "05:00",
            "min_price": 40000,
            "max_price": 70000,
            "latitude": 4.6530,
            "longitude": -74.0590,
            "music_genres": json.dumps(["Electrónica", "Pop", "Fusión"]),
            "rating": 4.9,
            "total_reviews": 1200
        },
        {
            "name": "Clandestino",
            "address": "Calle 84A # 12-50, Bogotá",
            "description": "Perfecto para los amantes de la salsa y la música latina.",
            "image_url": "https://example.com/clandestino.jpg",
            "phone": "+57 1 456 7890",
            "opening_time": "20:00",
            "closing_time": "03:00",
            "min_price": 25000,
            "max_price": 45000,
            "latitude": 4.6670,
            "longitude": -74.0530,
            "music_genres": json.dumps(["Salsa", "Latino", "Crossover"]),
            "rating": 4.7,
            "total_reviews": 380
        },
        {
            "name": "La Negra",
            "address": "Calle 100 #15-20, Bogotá",
            "description": "Ambiente caribeño y ritmos latinos para disfrutar con amigos.",
            "image_url": "https://example.com/lanegra.jpg",
            "phone": "+57 1 567 8901",
            "opening_time": "19:00",
            "closing_time": "02:00",
            "min_price": 20000,
            "max_price": 40000,
            "latitude": 4.6900,
            "longitude": -74.0450,
            "music_genres": json.dumps(["Latino", "Caribeña"]),
            "rating": 4.6,
            "total_reviews": 290
        },
        {
            "name": "Presea Bar",
            "address": "Cra 13 #50-60, Bogotá",
            "description": "El mejor after party con DJs de techno y ambiente underground.",
            "image_url": "https://example.com/presea.jpg",
            "phone": "+57 1 678 9012",
            "opening_time": "23:00",
            "closing_time": "06:00",
            "min_price": 35000,
            "max_price": 60000,
            "latitude": 4.6400,
            "longitude": -74.0650,
            "music_genres": json.dumps(["Techno", "After Party"]),
            "rating": 4.5,
            "total_reviews": 210
        }
    ]
    
    with app.app_context():
        # Verificar si ya existen bares
        existing_count = Bar.query.count()
        if existing_count > 0:
            print(f"Ya existen {existing_count} bares en la BD. ¿Deseas continuar? (s/n)")
            response = input().lower()
            if response != 's':
                print("Operación cancelada.")
                return
        
        # Insertar bares
        for bar_data in bars_data:
            # Verificar si ya existe por nombre
            existing = Bar.query.filter_by(name=bar_data['name']).first()
            if existing:
                print(f"Bar '{bar_data['name']}' ya existe. Saltando...")
                continue
            
            bar = Bar(**bar_data)
            db.session.add(bar)
            print(f"✓ Bar creado: {bar.name}")
        
        db.session.commit()
        print(f"\n✅ Proceso completado. Total de bares: {Bar.query.count()}")

if __name__ == "__main__":
    seed_bars()