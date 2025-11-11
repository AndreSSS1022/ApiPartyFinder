from repositories.user_repository import UserRepository
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class UserService:
    def __init__(self, session):
        self.session = session

    @staticmethod
    def register_user(username, password, full_name=None, birth_date=None, profile_image=None):
        from models.db import db
        from repositories.user_repository import UserRepository

        existing_user = UserRepository.get_by_username(username, db.session)
        if existing_user:
            return {"error": "Usuario ya existe"}

        hashed_password = generate_password_hash(password)

        parsed_date = None
        if birth_date:
            try:
                parsed_date = datetime.strptime(birth_date, "%Y-%m-%d").date()
            except Exception:
                parsed_date = None

        user = UserRepository.create_user(
            username=username,
            password=hashed_password,
            full_name=full_name,
            birth_date=parsed_date,
            profile_image=profile_image,
            session=db.session
        )
        return user

    @staticmethod
    def authenticate(username, password):
        from models.db import db
        from repositories.user_repository import UserRepository

        user = UserRepository.get_by_username(username, db.session)
        if user and check_password_hash(user.password, password):
            return user
        return None

    @staticmethod
    def get_all_users():
        from models.db import db
        from repositories.user_repository import UserRepository
        return UserRepository.get_all(db.session)
