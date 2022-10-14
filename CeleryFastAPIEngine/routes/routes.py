from fastapi import APIRouter

from routes import submission

api_router = APIRouter()

# Need to expose the router from submission to main
# First expose the router from submission, which can be seen below.
# Main can now import this from routes.routes through api_router (seen at top of main)
# As a result, we align with single responsibility principle
api_router.include_router(submission.router)
