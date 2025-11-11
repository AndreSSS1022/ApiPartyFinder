"""
Servicio para el modelo User.
Aquí se maneja la lógica de negocio relacionada con usuarios.
Puedes crear más servicios siguiendo este ejemplo.
"""

from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logger = logging.getLogger(__name__)

class UserService:

    @staticmethod
    def register_user(name, lastname, email, password, birthdate):
        from models.db import db
        logger.info(f'Registrando usuario en servicio: {name, lastname, email, birthdate}')
        # Validar si el usuario ya existe
        existing_user = UserRepository.get_by_username(email, db.session)
        if existing_user:
            logger.warning(f'Intento de registro con usuario existente: { email}')
            return {'error': 'Usuario ya existe', 'username': email}
        hashed_password = generate_password_hash(password)
        user = UserRepository.create_user( name, lastname, email, hashed_password, birthdate, db.session)
        logger.info(f'Usuario creado en servicio: {user.email} (ID: {user.id})')
        return user


    @staticmethod
    def authenticate(email, password):
        from models.db import db
        logger.info(f'Autenticando usuario en servicio: {email}')
        user = UserRepository.get_by_username(email, db.session)
        if user and check_password_hash(user.password, password):
            logger.info(f'Autenticación exitosa en servicio: {email}')
            return user
        logger.warning(f'Autenticación fallida en servicio: {email}')
        return None


    @staticmethod
    def get_all_users():
        from models.db import db
        logger.info('Obteniendo todos los usuarios en servicio')
        users = UserRepository.get_all(db.session)
        logger.info(f'{len(users)} usuarios obtenidos en servicio')
        return users

"""
Para crear más servicios:
1. Crea un archivo en la carpeta services (ejemplo: product_service.py).
2. Implementa la lógica de negocio para el modelo correspondiente.
"""
