#!/usr/bin/env python3
"""
AUTH METHOD FOR USERS
"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from typing import Optional


def _hash_password(password: str) -> bytes:
    """
    ENCRYPT PASSWORD
    """
    pass_bytes = password.encode()
    hash_passwd = bcrypt.hashpw(pass_bytes, bcrypt.gensalt())
    return hash_passwd


def _generate_uuid() -> str:
    """
    return generated uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class.
    """

    def __init__(self):
        """
        InitializER
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        add new user when possible
        """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(user.email))
        except (InvalidRequestError, NoResultFound):
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        compare passwords for equality to validate login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except (InvalidRequestError, NoResultFound):
            return False

    def create_session(self, email: str) -> Optional[str]:
        """
        session creater
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return user.session_id
        except Exception as e:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        retrieve user by session id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        session destroyer (ssid == None)
        """
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        reset token
        """
        try:
            user = self._db.find_user_by(email=email)
            reset_token = self._generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return user.reset_token
        except Exception as e:
            raise ValueError
