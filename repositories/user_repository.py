from sqlalchemy.orm import Session
from models.user import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    @staticmethod
    def get_by_username(username: str, session: Session):
        logger.info(f'Buscando usuario: {username}')
        user = session.query(User).filter_by(username=username).first()
        if user:
            logger.info(f'Usuario encontrado: {username}')
        else:
            logger.warning(f'Usuario no encontrado: {username}')
        return user

    @staticmethod
    def create_user(username: str, password: str, full_name: str, birth_date, profile_image: str, session: Session):
        """
        Crea un nuevo usuario con todos los campos requeridos.
        """
        logger.info(f'Creando usuario: {username}')
        user = User(
            username=username,
            password=password,
            full_name=full_name,
            birth_date=birth_date,
            profile_image=profile_image
        )
        session.add(user)
        session.commit()
        logger.info(f'Usuario creado con éxito: {username} (ID: {user.id})')
        return user

    @staticmethod
    def get_all(session: Session):
        logger.info('Obteniendo todos los usuarios')
        users = session.query(User).all()
        logger.info(f'{len(users)} usuarios encontrados')
        return users
