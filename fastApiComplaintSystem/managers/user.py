from fastapi import HTTPException
from passlib.context import CryptContext

from asyncpg import UniqueViolationError
from db import database
from managers.auth import AuthManager
from models import user, RoleType, complaint, State

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserManager:
    @staticmethod
    async def register(user_data):
        # Need to change the password to hash
        user_data["password"] = pwd_context.hash(user_data["password"])
        # Need to store in DB
        try:
            # Execute the user model with the passed in user_data
            id_ = await database.execute(user.insert().values(**user_data))
        except UniqueViolationError:
            raise HTTPException(400, "User exists already with this email")

        user_do = await database.fetch_one(user.select().where(user.c.id == id_))

        # Need to get a token for the user
        return AuthManager.encode_token(user_do)

    @staticmethod
    async def login(user_data):
        user_do = await database.fetch_one(
            user.select().where(user.c.email == user_data["email"])
        )
        if not user_do:
            raise HTTPException(400, "Wrong email")
        elif not pwd_context.verify(user_data["password"], user_do["password"]):
            raise HTTPException(400, "Wrong password")

        return AuthManager.encode_token(user_do)

    @staticmethod
    async def get_all_users():
        return await database.fetch_all(user.select())

    @staticmethod
    async def get_user_by_email(email):
        return await database.fetch_one(user.select().where(user.c.email == email))

    @staticmethod
    async def change_role(role: RoleType, user_id):
        await database.execute(
            user.update().where(user.c.id == user_id).values(role=role)
        )

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.approved)
        )

    @staticmethod
    async def reject(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.rejected)
        )
