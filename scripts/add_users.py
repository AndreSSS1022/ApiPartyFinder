"""
Script para agregar usuarios de ejemplo a la base de datos SQLite.
Ejecuta este archivo para poblar la tabla users con datos más completos.
"""
import os
from datetime import date
from flask import Flask
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

from models.db import db
from models.user import User

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///flaskapi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

usuarios = [
    {
        "username": "usuario1",
        "password": "password1",
        "full_name": "Carlos Pérez",
        "birth_date": date(1995, 3, 12),
        "profile_image": "https://i.pravatar.cc/150?img=1"
    },
    {
        "username": "usuario2",
        "password": "password2",
        "full_name": "María López",
        "birth_date": date(1998, 6, 25),
        "profile_image": "https://i.pravatar.cc/150?img=2"
    },
    {
        "username": "usuario3",
        "password": "password3",
        "full_name": "Juan Rodríguez",
        "birth_date": date(2000, 1, 8),
        "profile_image": "https://i.pravatar.cc/150?img=3"
    }
]

with app.app_context():
    db.create_all()
    for u in usuarios:
        if not User.query.filter_by(username=u["username"]).first():
            hashed_pw = generate_password_hash(u["password"])
            user = User(
                username=u["username"],
                password=hashed_pw,
                full_name=u["full_name"],
                birth_date=u["birth_date"],
                profile_image=u["profile_image"]
            )
            db.session.add(user)
    db.session.commit()

print("✅ Usuarios agregados correctamente con datos completos.")