from sqlalchemy.orm import Session
from models.user import User
import logging

logger = logging.getLogger(__name__)

class UserRepository:
    @staticmethod
    def get_by_username(username, session: Session):
        logger.info(f'Buscando usuario en repositorio: {username}')
        user = session.query(User).filter_by(username=username).first()
        if user:
            logger.info(f'Usuario encontrado: {username}')
        else:
            logger.warning(f'Usuario no encontrado: {username}')
        return user

    @staticmethod
    def create_user(username, password, full_name, birth_date, profile_image, session: Session):
        logger.info(f'Creando usuario en repositorio: {username}')
        user = User(
            username=username,
            password=password,
            full_name=full_name,
            birth_date=birth_date,
            profile_image=profile_image
        )
        session.add(user)
        session.commit()
        logger.info(f'Usuario creado en repositorio: {username} (ID: {user.id})')
        return user

    @staticmethod
    def get_all(session: Session):
        logger.info('Obteniendo todos los usuarios en repositorio')
        users = session.query(User).all()
        logger.info(f'{len(users)} usuarios obtenidos')
        return users
