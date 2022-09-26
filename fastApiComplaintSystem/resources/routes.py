from fastapi import APIRouter

from resources import auth, complaint

api_router = APIRouter()

# Need to expose the router /register from auth to main
# First expose the router from auth, which can be seen below.
# Main can now import this from resources.routes through api_router (seen at top of main)
# As a result, we align with single responsibility principle
api_router.include_router(auth.router)
api_router.include_router(complaint.router)
