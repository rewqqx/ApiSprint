from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy.orm import Session
from src.core.settings import settings
from src.db.db import get_session
from src.models.schemas.user.user_request import UserRequest
from src.models.schemas.utils.jwt_token import JwtToken
from src.models.user import User
import os


oauth2_schema = OAuth2PasswordBearer(tokenUrl='/users/authorize')


def get_current_user_id(token: str = Depends(oauth2_schema)) -> int:
    return UsersService.verify_token(token)


def check_admin(token: str = Depends(oauth2_schema)) -> int:
    role = UsersService.check_role(token)
    if role == 'admin':
        return UsersService.verify_token(token)
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="У вас нет прав для этого действия")


class UsersService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    @staticmethod
    def hash_password(password: str) -> str:
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def check_password(password_text: str, password_hash: str) -> bool:
        return pbkdf2_sha256.verify(password_text, password_hash)

    @staticmethod
    def verify_token(token: str) -> Optional[int]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

        return payload.get('sub')

    @staticmethod
    def check_role(token: str) -> Optional[str]:
        try:
            payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Некорректный токен")

        return payload.get('role')

    @staticmethod
    def create_token(user_id: int, user_role: str) -> JwtToken:
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'exp': now + timedelta(seconds=settings.jwt_expires_seconds),
            'sub': str(user_id),
            'role': user_role,
        }
        token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
        return JwtToken(access_token=token)

    def register(self, user_schema: UserRequest):
        user = User(
            username=user_schema.username,
            password_hashed=self.hash_password(user_schema.password_hashed),
            role=user_schema.role,
        )
        self.session.add(user)
        self.session.commit()
        user = self.get(user.id)
        setattr(user, 'created_by', user.id)
        setattr(user, 'modified_by', user.id)
        self.session.commit()

    def authorize(self, username: str, password_text: str) -> Optional[JwtToken]:
        user = (
            self.session
            .query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            return None
        if not self.check_password(password_text, user.password_hashed):
            return None

        return self.create_token(user.id, user.role)

    def all(self) -> List[User]:
        users = (
            self.session
            .query(User)
            .order_by(
                User.id.desc()
            )
            .all()
        )
        return users

    def get(self, user_id: int) -> User:
        user = (
            self.session
            .query(User)
            .filter(
                User.id == user_id,
            )
            .first()
        )
        return user

    def add(self, user_id: int, user_schema: UserRequest) -> User:
        user_dict = user_schema.dict()
        user_dict['created_by'] = user_id
        user_dict['modified_by'] = user_id
        user = User(**user_dict)
        self.session.add(user)
        self.session.commit()
        return user

    def update(self, user_req: int, user_id: int, user_schema: UserRequest) -> User:
        user = self.get(user_id)
        for field, value in user_schema:
            if field == 'password_hashed':
                value = self.hash_password(value)
            setattr(user, field, value)
        setattr(user, 'modified_by', user_req)
        self.session.commit()
        return user

    def delete(self, user_id: int):
        user = self.get(user_id)
        self.session.delete(user)
        self.session.commit()
