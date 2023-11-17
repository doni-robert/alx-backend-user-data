#!/usr/bin/env python3
""" The auth module """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
import uuid


def _hash_password(password: str) -> bytes:
    """
    Returns a hashed passwor in bytes
    """
    bytes_pwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash_pwd = bcrypt.hashpw(bytes_pwd, salt)

    return hash_pwd


def _generate_uuid() -> str:
    """
    Returns a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user
        """
        try:
            if self._db.find_user_by(email=email):
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hash_pwd = _hash_password(password)
            user = self._db.add_user(email, hash_pwd)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates a user's credentials
        """
        try:
            user = self._db.find_user_by(email=email)
            pwd_bytes = password.encode('utf-8')

            if bcrypt.checkpw(pwd_bytes, user.hashed_password):
                return True
            else:
                return False
        except (NoResultFound, InvalidRequestError) as e:
            return False

    def create_session(self, email: str) -> str:
        """
        creates a session for its user

        Return:
            Returns the session id
        """
        try:
            user = self._db.find_user_by(email=email)
            new_uuid = _generate_uuid()
            self._db.update_user(user.id, session_id=new_uuid)

            return new_uuid
        except Exception:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Retrieves a user using the session_id
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroys a user's session
        """
        if user_id is None:
            return None
        user = self._db.find_user_by(id=user_id)
        self._db.update_user(user, session_id, None)
