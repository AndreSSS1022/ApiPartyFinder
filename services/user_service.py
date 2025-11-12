from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from models.db import db
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserService:
    @staticmethod
    def register_user(username, password, full_name, birth_date, profile_image=None):
        """
        Registra un nuevo usuario verificando duplicados y encriptando contraseña.
        """
        session = db.session

        existing_user = UserRepository.get_by_username(username, session)
        if existing_user:
            logger.warning(f'Intento de registro con usuario existente: {username}')
            return None, "El usuario ya existe"

        try:
            hashed_password = generate_password_hash(password)
            birth_date_obj = datetime.strptime(birth_date, "%Y-%m-%d").date()

            user = UserRepository.create_user(
                username=username,
                password=hashed_password,
                full_name=full_name,
                birth_date=birth_date_obj,
                profile_image=profile_image,
                session=session
            )
            logger.info(f'Usuario registrado exitosamente: {username}')
            return user, None
        except Exception as e:
            session.rollback()
            logger.error(f'Error al registrar usuario: {str(e)}')
            return None, "Error al registrar usuario"

    @staticmethod
    def authenticate(username, password):
        """
        Valida las credenciales del usuario.
        """
        session = db.session
        user = UserRepository.get_by_username(username, session)
        if user and check_password_hash(user.password, password):
            logger.info(f'Usuario autenticado: {username}')
            return user
        else:
            logger.warning(f'Autenticación fallida: {username}')
            return None
