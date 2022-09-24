from fastapi import APIRouter

from managers.user import UserManager

router = APIRouter(tags=["Auth"])


# Saves the user into the database and passes to authenication manager
# Authentication manager should return the login token
@router.post("/register/", status_code=201)
async def register(user_data):
    token = UserManager.register(user_data)
    return {"token": token}
