from fastapi import HTTPException
from passlib.context import CryptContext

from asyncpg import UniqueViolationError
from db import database
from managers.auth import AuthManager
from models import user

pwd_context = CryptContext(scheme=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        # Need to change the password to hash
        user_data["password"] = pwd_context.hash(user_data["password"])
        # Need to store in DB
        try:
            # Execute the user model with the passed in user_data
            id_ = await database.execute(user().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User exists already with this email")

        user_do = await database.fetch_one(user.select().where(user.c.id == id_))

        # Need to get a token for the user
        return AuthManager.encode_token(user_do)
